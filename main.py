import requests
import time
import asyncio
from dev import html_scraper, url_collection
from codecarbon import EmissionsTracker

def main() -> None:
    with EmissionsTracker(project_name="carbon_tracking") as tracker:
        start = time.time()
        # 1. scrape urls of all provinces
        results = asyncio.run(url_collection.provinces_url ())

        # 2. save urls to output file
        url_output_file = "all_properties.txt"
        url_collection.save_to_file(results, url_output_file)
        print(f"Saved {sum(len(v) for v in results.values())} urls in {time.time()-start:.1f} s.")

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

<<<<<<< HEAD
    # save properties data to file
    data_output_file = "properties.csv"
    html_scraper.ImmoVlanScraper.to_csv_file(data_output_file, list(properties_data.values()))

    print(f"Scraped {len(properties_data)} properties data, it took {time.time() - start:.1f} sec.")
=======
        # save properties data to file
        data_output_file = "propertyData.csv"
        html_scraper.ImmoVlanScraper.to_csv_file(data_output_file, properties_data)
        print(f"Scraped {len(properties_data)} properties data, it took {time.time() - start:.1f} sec.")
    
    print(f"Total emissions: {tracker.final_emissions*1000:.4f} g CO2eq")
>>>>>>> 0650c842ec6c18ea31685c6c88121f37c94ca105

if __name__ == "__main__":
    main()