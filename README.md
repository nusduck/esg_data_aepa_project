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
   ```

3. Edit `demo_config.yaml` to add your model and API key and rename this file to `config.yaml`.

4. Move your reports file to `data/esg_reports_pdf` directory.

5. Run the script to parse ESG reports:

   ```shell
   python3 src/pdf_parse/llm_parse_esg_reports_pdf.py
   ```