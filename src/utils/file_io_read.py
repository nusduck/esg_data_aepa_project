import os
def read_pdf(pdf_dir, specific_report=None):
    pdf_path = []
    if specific_report:
        specific_file = os.path.join(pdf_dir, specific_report) # ABC company_report.pdf
        pdf_path.append(specific_file)
    else:
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                pdf_onefile = os.path.join(pdf_dir, filename)
                pdf_path.append(pdf_onefile)
                print(pdf_onefile)
    return pdf_path
# read directory of path
def read_dir(dir_path,specific_report=None):
    if specific_report:
        # remove the .pdf extension
        specific_report = specific_report.split('.')[0]
        specific_file = specific_report
        return specific_file
    else:
        filenames  = []
        for filename in os.listdir(dir_path):
            if filename != '.DS_Store':
            
                filenames.append(filename)
        return filenames
# read txt files in a directory and pass the specific_report=None to the function
def read_text(txt_dir, specific_report=None):
    if specific_report:
        # replace the .pdf extension with .txt
        specific_report = specific_report.replace('.pdf', '.txt')
        specific_file = os.path.join(txt_dir, specific_report)
        return specific_file
    else:
        files = []
        for filename in os.listdir(txt_dir):
            if filename.endswith('.txt'):
                txt_onefile = os.path.join(txt_dir, filename)
                files.append(txt_onefile)
        return files
  
def read_company_names(data_folder, specific_report=None):
        company_names = []
        if specific_report:
            # Extract company name from filename (remove '_report.txt')
            company_name = specific_report.replace('_report.pdf', '')
            company_names.append(company_name)
        else:
            for file_path in os.listdir(data_folder):
                # Extract company name from filename (remove '_report.txt')
                if file_path != '.DS_Store':
                    company_name = file_path.replace('_report.txt', '')
                    company_names.append(company_name)
                
        return company_names
if __name__ == '__main__':
    pdf_dir = 'data/esg_reports_pdf'
    base_output_dir = 'data/output'
    pdf_path = read_pdf(pdf_dir, specific_report='ABC_company_report.pdf')
    a = read_dir("data/esg_parse_result")
    b = read_text("data/esg_cleaned_data", )
    c = read_company_names("data/esg_cleaned_data")
    print(a)