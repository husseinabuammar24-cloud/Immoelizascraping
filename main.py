import requests
import time
import asyncio

from dev import html_scraper, url_collection

def main() -> None: 
  
    start = time.time()
    # 1. scrape urls of all provinces
    results = asyncio.run(url_collection.provinces_url (pages=5))

    # 2. save urls to output file
    url_output_file = "all_properties.txt"
    url_collection.save_to_file(results, url_output_file)
    print(f"Saved {sum(len(v) for v in results.values())} urls in {time.time()-start:.1f} s.")

    for key, urls in results.items():
        for url in urls:
            session = requests.Session()
            immovlan_scraper = html_scraper.ImmoVlanScraper(session)
            html = immovlan_scraper.fetch_html(url)
            propertyData = immovlan_scraper.get_data(html)

            html_scraper.ImmoVlanScraper.to_json_file("propertyData.json", propertyData)
    
if __name__ == "__main__":
    main()