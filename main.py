import requests

from dev import html_scraper
from dev.url_collection import provinces_url, save_to_file

def main() -> None: 
  
    results = provinces_url ()       # 1. scrape all provinces
    save_to_file(results)              # 2. save to file

    for url in results:
      session = requests.Session()

      immovlan_scraper = html_scraper.ImmoVlanScraper(session)
      html = immovlan_scraper.fetch_html(url)
      propertyData = immovlan_scraper.get_data(html)

      html_scraper.ImmoVlanScraper.to_json_file("propertyData.json", propertyData)
    
if __name__ == "__main__":
    main()