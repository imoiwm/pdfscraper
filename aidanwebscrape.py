"""# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')
 
# Find all hyperlinks present on webpage
links = soup.find_all('a')
 
i = 0
 
# From all links check for pdf link and
# if present download file
for link in links:
    if ('.pdf' in link.get('href', [])):
        i += 1
        print("Downloading file: ", i)
 
        # Get response object for link
        response = requests.get(link.get('href'))
 
        # Write content in pdf file
        pdf = open(str(link)+".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        print("File ", i, " downloaded")
 """


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

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

driver = webdriver.Chrome()
driver.get("https://families.decal.ga.gov/ChildCare/detail/15173")
#assert "Python" in driver.title
for b in driver.find_elements(By.XPATH, "//a[@title='View Inspection Report']"):
    print("what")
    print(b)
    b.click()
assert "No results found." not in driver.page_source
download_wait()
driver.close()

print("All PDF files downloaded")