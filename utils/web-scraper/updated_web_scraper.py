import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
from selenium import webdriver

WEBDRIVER_PATH = "ENTER WEBDRIVER PATH"

def scrape(url):
    # start web browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser=webdriver.Chrome(executable_path=WEBDRIVER_PATH, options=options)
    browser.set_page_load_timeout(20)
    # get source code
    browser.get(url)
    content = browser.page_source
    browser.close()
    
    soup = BeautifulSoup(content, "html5lib")
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # Filter out hyperlinks (<a/> tags) that are not enclosed by regular text (parent element = <p/> tag)
    tags_to_discard = filter(lambda x: x.parent.name != 'p', soup.select("a"))
    for tag in tags_to_discard:
        tag.extract()

    return_text = soup.get_text(strip=True)

    return return_text

def process_csv_results(csv_file, write_to_csv=True):
    with open(csv_file, 'r') as f:
        csv_obj = csv.reader(f)
        for idx, row in enumerate(csv_obj):
            if idx > 0:
                print(row[2])
                company_name = str.split(row[0])[0].lower()
                try:
                    scrape_result = scrape(row[2]).lower()
                except Exception as e:
                    print(e)
                    scrape_result = row[4]
                name_in_scrape = company_name in scrape_result
                print(name_in_scrape, company_name)
                return name_in_scrape
