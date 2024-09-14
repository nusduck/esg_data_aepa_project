import ssl
import csv
import time
import re
import urllib
import os
import sys
from datetime import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote
import curl_cffi.requests as requests

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize log file
timee = str(datetime.now())
log_file = 'src/download_record/down_loadlog.csv'
with open(log_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Keyword', 'Download Success', 'URL', 'Local File Path', 'Search Link'])

# Function to download PDF for a given keyword
def download_pdf(keyword):
    query = keyword.replace(' ', '+') + '+pdf'
    name = 'data/esg_reports_pdf'

    # Create folder for storing PDF files
    os.makedirs(name, exist_ok=True)

    # Set user agent
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    # Construct search link
    search_link = f'https://www.google.com/search?q=filetype%3Apdf+{query}+sustainability+report+2022&start=0'

    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(search_link, None, headers)

    try:
        html = urllib.request.urlopen(request)
        soup = BeautifulSoup(html, 'lxml')

        # Parse search results
        po = soup.find_all(href=re.compile("http://|https://"))

        # Find the first non-ad PDF file and download
        for i in po:
            io = i.encode('utf-8')
            searchObj = re.search(r'(http[s]?://.*?\.pdf)', str(io), re.M | re.I)
            if searchObj:
                realink = unquote(searchObj.group(1))  # URL decode the link
                titlee = os.path.join(name, f"{keyword}_report.pdf")
                try:
                    response = requests.get(realink, verify=False, impersonate="chrome101")
                    with open(titlee, 'wb') as f:
                        f.write(response.content)
                    log_result(keyword, 1, realink, titlee, search_link)
                    return True  # Exit after successful download
                except Exception as e:
                    print(f"Failed to download {realink}: {e}")
                    log_result(keyword, 0, realink, '', search_link)
                    return False

        print(f"No suitable PDF found for {keyword}")
        log_result(keyword, 0, '', '', search_link)
        return False
    except Exception as e:
        print(f"Error processing {keyword}: {e}")
        log_result(keyword, 0, '', '', search_link)
        return False

def log_result(keyword, success, url, file_path, search_link):
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), keyword, success, url, file_path, search_link])

# Main function to control the download process
def main(start_row=2, batch_size=5, pause_time=60):
    csv_file = 'ESG/CompanyList.csv'
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    total_rows = len(rows) - (start_row - 1)
    if start_row > len(rows):
        print(f"Start row {start_row} is greater than total rows {len(rows)}. Exiting.")
        return

    print(f"Starting downloads from row {start_row}")

    # Overall progress bar
    with tqdm(total=total_rows, desc="Download Progress", unit="company") as pbar:
        for i, row in enumerate(rows[start_row-1:], start=start_row):
            if row:  # Check if the row is not empty
                keyword = row[0]  # Get the first column
                success = download_pdf(keyword)
                pbar.update(1)
                if success:
                    pbar.set_postfix_str("Success")
                else:
                    pbar.set_postfix_str("Failed")

            # Check if we need to pause
            if (i - start_row + 1) % batch_size == 0 and i < len(rows) - 1:
                print(f"Completed batch. Pausing for {pause_time} seconds...")
                time.sleep(pause_time)

    print(f"Process completed. Check {log_file} for details.")

if __name__ == "__main__":
    # You can change these values as needed
    start_row = 2  # Start from the second row (change this to start from a different row)
    batch_size = 5  # Number of downloads before pausing
    pause_time = 0  # Pause time in seconds

    main(start_row, batch_size, pause_time)