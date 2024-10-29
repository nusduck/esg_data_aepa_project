import numpy as np
import faiss
import os
import json
import pickle
from mistralai import Mistral
import time
import glob

class MultiFileRAG:
    def __init__(self, api_key, input_dir="data/esg_cleaned_data", output_dir="data/esg_vector_data"):
        self.client = Mistral(api_key=api_key)
        self.chunk_size = 2048
        self.input_dir = input_dir
        self.embeddings_dir = output_dir
        self.ensure_directory()
        
    def ensure_directory(self):
        """Create embeddings directory if it doesn't exist"""
        if not os.path.exists(self.embeddings_dir):
            os.makedirs(self.embeddings_dir)
            
    def get_processed_files(self):
        """Get list of files that have already been processed"""
        processed_files = set()
        for filepath in glob.glob(os.path.join(self.embeddings_dir, "*_embeddings.npy")):
            base_name = os.path.basename(filepath)
            # Remove '_embeddings.npy' to get original file id
            file_id = base_name[:-14]  
            processed_files.add(file_id)
        return processed_files
    
    def get_text_embedding(self, input_text):
        """Get embedding for a text using Mistral API"""
        embeddings_response = self.client.embeddings.create(
            model="mistral-embed",
            inputs=input_text
        )
        return embeddings_response.data[0].embedding
    
    def chunk_text(self, text):
        """Split text into chunks"""
        return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]
    
    def process_all_files(self):
        """Process all txt files in the input directory"""
        # Get list of already processed files
        processed_files = self.get_processed_files()
        
        # Get all txt files in input directory
        txt_files = glob.glob(os.path.join(self.input_dir, "*.txt"))
        
        for file_path in txt_files:
            file_id = os.path.basename(file_path)[:-4]  # Remove .txt extension
            
            # Skip if already processed
            if file_id in processed_files:
                print(f"Skipping {file_id} - already processed")
                continue
                
            print(f"Processing {file_id}...")
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                
                # Process file
                self.process_file(file_id, text_content)
                print(f"Successfully processed {file_id}")
                
            except Exception as e:
                print(f"Error processing {file_id}: {str(e)}")
    
    def process_file(self, file_id, text_content):
        """Process a single file and save its embeddings"""
        # Chunk the text
        chunks = self.chunk_text(text_content)
        
        # Get embeddings with rate limiting
        embeddings = []
        chunk_map = []  # Store chunk text and its position
        
        for i, chunk in enumerate(chunks):
            try:
                embedding = self.get_text_embedding(chunk)
                embeddings.append(embedding)
                chunk_map.append({
                    'position': i,
                    'text': chunk
                })
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"Error processing chunk {i} of {file_id}: {str(e)}")
                continue
            
        # Convert to numpy array
        embeddings_array = np.array(embeddings)
        
        # Save embeddings and chunk map
        self.save_file_data(file_id, embeddings_array, chunk_map)
        
        return embeddings_array, chunk_map
    
    def save_file_data(self, file_id, embeddings_array, chunk_map):
        """Save embeddings and chunk map for a file"""
        file_path = os.path.join(self.embeddings_dir, f"{file_id}")
        
        # Save embeddings using numpy
        np.save(f"{file_path}_embeddings.npy", embeddings_array)
        
        # Save chunk map using pickle
        with open(f"{file_path}_chunks.pkl", 'wb') as f:
            pickle.dump(chunk_map, f)
    
    def load_file_data(self, file_id):
        """Load embeddings and chunk map for a file"""
        file_path = os.path.join(self.embeddings_dir, f"{file_id}")
        
        # Load embeddings
        embeddings_array = np.load(f"{file_path}_embeddings.npy")
        
        # Load chunk map
        with open(f"{file_path}_chunks.pkl", 'rb') as f:
            chunk_map = pickle.load(f)
            
        return embeddings_array, chunk_map
    
    def search(self, question, file_ids=None, k=2):
        """
        Search across specified files or all files if file_ids is None
        """
        # If no file_ids specified, use all processed files
        if file_ids is None:
            file_ids = list(self.get_processed_files())
            
        # Get question embedding
        question_embedding = np.array([self.get_text_embedding(question)])
        
        # Collect all relevant embeddings and chunks
        all_embeddings = []
        all_chunks = []
        current_position = 0
        file_positions = {}  # Track where each file's embeddings start
        
        for file_id in file_ids:
            try:
                embeddings, chunk_map = self.load_file_data(file_id)
                file_positions[file_id] = {
                    'start': current_position,
                    'end': current_position + len(embeddings)
                }
                all_embeddings.append(embeddings)
                all_chunks.extend(chunk_map)
                current_position += len(embeddings)
            except Exception as e:
                print(f"Error loading data for {file_id}: {str(e)}")
                continue
        
        if not all_embeddings:
            raise ValueError("No valid embeddings found for the specified files")
            
        # Combine all embeddings
        combined_embeddings = np.concatenate(all_embeddings)
        
        # Create FAISS index
        d = combined_embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(combined_embeddings)
        
        # Search
        D, I = index.search(question_embedding, k)
        
        # Get results with file information
        results = []
        for idx in I[0]:
            for file_id, positions in file_positions.items():
                if positions['start'] <= idx < positions['end']:
                    results.append({
                        'file_id': file_id,
                        'chunk': all_chunks[idx]['text']
                    })
                    break
        
        return results
    
    def query(self, question, file_ids=None, model="mistral-large-latest"):
        """Query the system with a question"""
        # Get relevant chunks
        try:
            relevant_chunks = self.search(question, file_ids)
            
            # Prepare prompt
            context = "\n".join([f"[From {r['file_id']}]:\n{r['chunk']}" for r in relevant_chunks])
            prompt = f"""
            Context information is below.
            ---------------------
            {context}
            ---------------------
            Given the context information and not prior knowledge, answer the query.
            Query: {question}
            Answer:
            """
            
            # Get response from Mistral
            messages = [{"role": "user", "content": prompt}]
            chat_response = self.client.chat.complete(
                model=model,
                messages=messages
            )
            
            return chat_response.choices[0].message.content
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Example usage:

# Initialize
rag = MultiFileRAG(api_key="your_api_key")

# Process all files in the input directory
rag.process_all_files()

# Query specific files or all files
question = "What is the company's environmental policy?"
# Query specific files
answer1 = rag.query(question, file_ids=["United Overseas Bank Limited_report", "United Overseas Insurance Limited_report"])
# Query all files
answer2 = rag.query(question)
