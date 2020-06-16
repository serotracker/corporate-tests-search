import requests
from bs4 import BeautifulSoup


def scrape(url, output_file_path="scraped_website"):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Filter out hyperlinks (<a/> tags) that are not enclosed by regular text (parent element = <p/> tag)
    tags_to_discard = filter(lambda x: x.parent.name != 'p', soup.select("a"))
    for tag in tags_to_discard:
        tag.extract()

    # Get text and save it to a txt file
    with open(f"{output_file_path}.txt", "w") as f:
        f.write(soup.get_text(strip=True))
    return


def main():
    url = "https://www.companynewshq.com/company-news/food-and-drink-company-news/tyson-foods-inc-releases-results-from-covid-19-testing-at-berry-street-facility-in-springdale-ar/"
    scrape(url)


if __name__ == '__main__':
    main()
