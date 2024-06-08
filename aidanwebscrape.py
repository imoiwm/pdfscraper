from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import csv

"""
This program is run by downloading the Python file
and then running it using the following command
(note the $ at the beginning is to denote the command line):

$ python aidanwebscrape.py {.csv filename}


TODO: see if we can move the files to a specific folder instead of just Downloads
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

def providers_from_csv(filename):
    res = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            res.append(row['provider_number'])

"""
Where the primary logic is performed
Scrapes all PDFs and downloads them into the same directory as this Python program
given a .csv file containing the fieldnames 'Count,' 'Provider_Number', and 'Location' in the first line
followed by each entry's three fieldname parameters on each new line

Note that for your purposes with DECAL, 
this can be done by exporting the spreadsheet in Google Sheets
(didn't test for Microsoft Excel) as a .csv
"""
def decal_pdfs(providers):
    # Prefix URLs for the search results and the provider breakdown pages, respectively
    search_url = "https://families.decal.ga.gov/ChildCare/Results?name="
    base_url = "https://families.decal.ga.gov/ChildCare/"

    driver = webdriver.Chrome()
    for pn in providers:
        driver.get(search_url + pn)

        # Handles case of multiple search results for provider number just as precaution
        # Otherwise, main purpose is to grab the link from clicking on the "View" button in the search results
        detail_suffix = []
        for result in driver.find_elements(By.XPATH, "//a[@data-track-name='View Provider - Button']"):
            detail_suffix.append(result.get_attribute('href'))

        # For each URL grabbed from the "View" buttons in the search results
        for ds in detail_suffix:
            # Left in a total recorded count of PDFs downloaded for troubleshooting purposes
            count = 0

            # Generate the page from the specified URL
            driver.get(ds)

            # Have Selenium click to download each PDF under the "Inspection Report" section
            for b in driver.find_elements(By.XPATH, "//a[@title='View Inspection Report']"):
                count += 1
                b.click()
            assert "No results found." not in driver.page_source

            # Wait to make sure all downloads complete
            download_wait()
            print(f"Downloaded {count} files from provider number {pn}")
        driver.close()


if __name__ == "__main__":
    #provider_number = input("Please input the DECAL provider number: ")

    #TODO this line takes in the filename passed as a function parameter
    #TODO need to test this program on a smaller subset of the initial .csv
    provider_numbers = providers_from_csv(filename)
    decal_pdfs(provider_numbers)