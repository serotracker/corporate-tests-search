import requests
from bs4 import BeautifulSoup
import csv
import argparse
import os


def scrape(url, output_file_path=None):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Filter out hyperlinks (<a/> tags) that are not enclosed by regular text (parent element = <p/> tag)
    tags_to_discard = filter(lambda x: x.parent.name != 'p', soup.select("a"))
    for tag in tags_to_discard:
        tag.extract()

    return_text = soup.get_text(strip=True)

    # Get text and save it to a txt file
    with open(f"{output_file_path}.txt", "w") as f:
        f.write(return_text)
    return return_text

def score_text(text, company_name):
    pass

def process_csv_results(csv_file, write_to_csv=True, dump_txts=True):
    print(csv_file, write_to_csv, dump_txts)
    # If dump_txts = true, create a 'results' folder
    if dump_txts:
        if not os.path.exists("results"):
            os.makedirs("results")
    # Open csv file
    with open(csv_file, 'r') as f:
        csv_obj = csv.reader(f)
        for idx, row in enumerate(csv_obj):
            if idx > 0:
                print(row)
    # Iterate through each row (after the first)
        # Get the url
        # call scrape(url) and get the text
        # if dump_txts, save it to a txt file
        # if write_to_csv, call score_text(text, company_name) and write to csv
    # Save the csv


def main():
    parser = argparse.ArgumentParser(description='score relevance of results in a provided csv file')
    parser.add_argument("csv_file", help="csv file to process")
    parser.add_argument("--write_to_csv", help="write results to csv or not", action='store_true')
    parser.add_argument("--dump_txts", help="save scraped text or not", action='store_true')

    args = parser.parse_args()
    process_csv_results(args.csv_file, args.write_to_csv, args.dump_txts)


if __name__ == '__main__':
    main()
