# Automated ESG Data Extraction and Performance Analysis

## Data Collection and Preprocessing

### Parsing Sustainability Reports

**Note:** Ensure your working directory is set to `esg_data_aepa_project`.

1. Clone the repository:

   ```shell
   git clone <repository_url>
   ```

2. Create a virtual environment and install the required libraries:

   ```shell
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   pip install -r requirements.txt
   export PYTHONPATH=$PYTHONPATH:. # Set your python path
   ```

3. Edit `demo_config.yaml` to add your model and API key and rename this file to `config.yaml`.

4. Move your reports file to `data/esg_reports_pdf` directory.

5. Run the script to extract ESG reports:

   ```shell
   python3 main.py --report example.pdf
   ```

   ### Filtered ESG report txt file

1. Download the pytoch for your GPU (Download to your desired virtual environment）
   
   Go to the official PyTorch website https://pytorch.org/get-started/locally/

2. Download the transformers library in your virtual environment.
   ```shell
   pip install transformers
   ```
   ```shell
   #If you have conda, you can run
   conda install transformers
   ```

3. View and run `src/filterdata/SimpleFilter.ipynb`

   ### Finetune BERT
1. Download the model.safetensors to `src/finetuned_model/`

   link: https://nusu-my.sharepoint.com/:u:/r/personal/e1351210_u_nus_edu/Documents/DSS5105-Project/model.safetensors?csf=1&web=1&e=7lomcZ
   
3. View and run `src/BERT/SimpleBERT.ipynb`

   ### Scoring

1. Run the script to generate ESG scores:

   ```shell
   python3 src/Scoring/esg_scoring.py
   ```
