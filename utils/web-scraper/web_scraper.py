import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://toronto.ctvnews.ca/ontario-government-asked-to-take-over-woodbridge-nursing-home-after-18-' \
          'residents-taken-to-hospital-1.4962347?cache=yes%3Fot%3DAjaxLayout%3FautoPlay%3Dtrue'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    with open("scraped_website.html", "w") as f:
        f.write(soup.get_text(strip=True))
    return


if __name__ == '__main__':
    main()
