import requests
import time

from dev import html_scraper
from dev.url_collection import provinces_url, save_to_file

def main() -> None: 

    start = time.time()
    # scrape urls
    results = provinces_url ()

    # save urls to file
    url_output_file = "all_properties.txt"
    save_to_file(results, url_output_file)
    print(f"Retrieved properties urls, it took {time.time() - start:.1f} sec.")

    start = time.time()
    properties_data = {}
    session = requests.Session()
    # scrape properties data
    with open(url_output_file,"r") as file:
        for url in file.readlines():
            ref = url.strip().split("/")[-1]
            immovlan_scraper = html_scraper.ImmoVlanScraper(session)
            html = immovlan_scraper.fetch_html(url)
            prop_data = immovlan_scraper.get_data(html)
            if len(prop_data):
                properties_data[ref] = prop_data

    # save properties data to file
    data_output_file = "propertyData.json"
    html_scraper.ImmoVlanScraper.to_json_file(data_output_file, properties_data)
    print(f"Scraped {len(properties_data)} properties data, it took {time.time() - start:.1f} sec.")

if __name__ == "__main__":
    main()