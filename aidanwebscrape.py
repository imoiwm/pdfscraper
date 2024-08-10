from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import csv
import sys
from threading import Thread
import queue

"""
Prerequisite downloads:

- Make sure Python is installed
- This Python file
- Download your provider list from Excel as a .csv file

First, modify the num_threads variable to match the number of cores on your CPU.
You can check how many cores there are by running the following lines in Python:
>> import multiprocessing
>> cpu_count = multiprocessing.cpu_count()
>> print(cpu_count)

Then run this program using the following command and replacing "{.csv filename}" with the actual filename, leaving out the curly braces:
(note the $ at the beginning is to denote the command line):

$ python aidanwebscrape.py {.csv filename}

The files will download to a folder called "InspectionReports" in the same directory as the program itself.

NOTE: This program took what I approximated to be an hour or two for about 250 providers in a sample .csv I ran.
I would suggest that, unless you want to run this program and babysit the computer for 40-50 hours,
that you chunk out sections of the full provider list into their own .csv files and then run it over those.
Let me know if you come across any other issues/problems/requests with the program. Thank you!

TODO: 
- Remove occasional errors
"""



"""
Taken from 
https://stackoverflow.com/questions/34338897/python-selenium-find-out-when-a-download-has-completed

Waits until Chrome download of PDF has completed
or 20 seconds have passed
in order to avoid incomplete download files being left behind
"""
def download_wait():
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(os.getcwd()):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds



"""
Given a .csv file, returns a list of its provider numbers.
See the notes below for decal_pdfs() for .csv file formatting
"""
def providers_from_csv(arr, filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            arr.append(row['Provider_Number'])



"""
Where the primary logic is performed
Scrapes all PDFs and downloads them into the same directory as this Python program
given a .csv file containing the fieldnames 'Count,' 'Provider_Number', and 'Location' in the first line
followed by each entry's three fieldname parameters on each new line

Note that for your purposes with DECAL, 
this can be done by exporting the spreadsheet in Google Sheets
(didn't test for Microsoft Excel) as a .csv
"""
def start_threads(providers):

    # Create a directory to save the PDFs if it doesn't exist
    
    url_queue = queue.Queue()
    for url in providers:
        url_queue.put(url)

    # Worker function to process URLs from the queue
    def worker():
        while not url_queue.empty():
            url = url_queue.get()
            try:
                os.makedirs(url, exist_ok=True)
                download_pdfs(url)
            finally:
                url_queue.task_done()

    # Number of threads
    num_threads = 12  # Adjust based on your system capabilities

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        

def download_pdfs(urlAdd):
    # Prefix URL for the search results
    search_url = "https://families.decal.ga.gov/ChildCare/Results?name="

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=1")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--ignore-certificate-errors')
    prefs = {"download.default_directory": os.path.join(os.getcwd(), urlAdd), "profile.managed_default_content_settings.images": 2, 'browser.helperApps.neverAsk.saveToDisk': 'application/pdf'}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    #driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": "C:/Users/Warren/Downloads"})
    driver.get(search_url + urlAdd)

    # Array and for ds loop below handle case of multiple search results for provider number just as precaution
    # Otherwise, main purpose is to grab the link from clicking on the "View" button in the search results
    detail_suffix = []
    for result in driver.find_elements(By.XPATH, "//a[@data-track-name='View Provider - Button']"):
        detail_suffix.append(result.get_attribute('href'))

    # For each URL grabbed from the "View" buttons in the search results
    for ds in detail_suffix:
        # Left in a total recorded count of PDFs downloaded for troubleshooting purposes
        count = 0
        
        driver.get(ds)

        # Have Selenium click to download each PDF under the "Inspection Report" section
        for b in driver.find_elements(By.XPATH, "//a[@title='View Inspection Report']"):
            b.click()
            count += 1
        
        download_wait()
        print(f"Downloaded {count} files from provider {urlAdd}")
    driver.close()
      



if __name__ == "__main__":
    provider_numbers = []
    
    providers_from_csv(provider_numbers, sys.argv[1])
    print(f"Loaded {len(provider_numbers)} providers")
    start_threads(provider_numbers)
    print("Download Complete!")