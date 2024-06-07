from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

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

provider_number = input("Please input the DECAL provider number: ")

# Prefix URLs for the search results and the provider breakdown pages, respectively
search_url = "https://families.decal.ga.gov/ChildCare/Results?name="
base_url = "https://families.decal.ga.gov/ChildCare/"


driver = webdriver.Chrome()
driver.get(search_url + provider_number)

"""
Handles case of multiple search results for provider number
just as precaution

Otherwise, main purpose is to grab the link 
from clicking on the "View" button in the search results
"""
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
    print(f"Downloaded {count} files from provider number {provider_number}")
driver.close()

