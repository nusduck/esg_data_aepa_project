from fastapi import FastAPI, HTTPException
import subprocess
import logging

app = FastAPI()


@app.post('/run-process')
async def run_process():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        logging.info('Starting all steps...')
        
        logging.info('Running llm_parse_esg_reports_pdf.py...')
        subprocess.run(['python', 'src/pdf_parse/llm_parse_esg_reports_pdf.py'], check=True)
        
        logging.info('Running txt_clean.py...')
        subprocess.run(['python', 'src/data_clean/txt_clean.py'], check=True)
        
        logging.info('Running Filter.py...')
        subprocess.run(['python', 'src/data_filter/Filter.py'], check=True)
        
        logging.info('Running llm_label.py...')
        subprocess.run(['python', 'src/label/llm_label.py'], check=True)
        
        logging.info('All steps completed successfully!')
       
        return {
            'message': 'Process completed successfully!'
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e.stderr}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)


    
