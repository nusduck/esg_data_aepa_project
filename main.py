import argparse
from src.pdf_parse.llm_parse_esg_reports_pdf import process_all_pdfs
from src.cleandata.esg_data_clean import esg_data_clean
from src.retrieve.esg_data_retrieve_by_context import esg_data_retrieve
from src.greenwash.llm_washgreen_detect import esg_washgreen_check
from src.realtime.llm_esg_realtime_info_search import esg_realtime_obtain


def parse_args():
    parser = argparse.ArgumentParser(description='ESG Data Retrieval Tool')
    parser.add_argument(
        '--report',
        type=str,
        default=None,
        help='Specific report file name to process (e.g. "report.pdf")'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    specific_report = args.report
    pdf_dir = 'data/esg_reports_pdf'
    process_all_pdfs(pdf_dir, verbose=True, gemini_worker=1, specific_report=specific_report) # parse pdfs
    esg_data_clean(specific_report=specific_report) # clean data
    esg_data_retrieve(specific_report=specific_report) # retrieve data
    esg_washgreen_check(specific_report=specific_report) # greenwash check
    esg_realtime_obtain(specific_report=specific_report) # real-time info search


if __name__ == '__main__':
    main()