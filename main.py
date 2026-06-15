import requests
from dev import html_scraper

def main() -> None: 

    session = requests.Session()
    url = "https://immovlan.be/en/detail/apartment/for-sale/5100/jambes/vbe35115"

    immovlan_scraper = html_scraper.ImmoVlanScraper(session)
    html = immovlan_scraper.fetch_html(url)
    propertyData = immovlan_scraper.get_data(html)

    html_scraper.ImmoVlanScraper.to_json_file("propertyData.json", propertyData)

if __name__ == "__main__":
    main()