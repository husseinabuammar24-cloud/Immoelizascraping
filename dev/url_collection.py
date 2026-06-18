import requests
from bs4 import BeautifulSoup
import asyncio

PROVINCES = [
    "Brussels", "Liège", "Vlaams-Brabant", "Namur", "Hainaut",
    "Brabant Wallon", "Limburg", "East Flanders", "Luxembourg",
    "West Flanders", "Antwerp"
]

TRANSACTIONS = ["rent", "sale"]


async def provinces_url(provinces=PROVINCES, pages=50, transactions=TRANSACTIONS) -> dict:
    """
    Method to collect property URLs for each province and page.

    :param provinces: List of provinces to scrape, default is 11 provinces in Belgium.
    :param pages: Number of pages to scrape for each province, default is 50.
    :param delay: Delay in seconds between requests to avoid overwhelming the server, default is 5 seconds.
    :param transactions: List of transaction types to scrape, default is ["rent", "sale"].
    :return: A dictionary containing property URLs categorized by province.
    """
    all_results = {}
    semaphore = asyncio.Semaphore(10)

    for t in transactions:

        for p in provinces:
            all_urls = []

            async def worker(worker_id:int):
                async with semaphore:
                    url = (
                        f"https://immovlan.be/en/real-estate?"
                        f"transactiontypes=for-{t}&propertytypes=house,apartment"
                        f"&provinces={p}&page={worker_id}&noindex=1"
                    )
                    # Make the HTTP request with a user-agent header to avoid blocking
                    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

                    # Check if the request was successful before parsing
                    if req.status_code == 200:
                        soup = BeautifulSoup(req.text, "html.parser")
                        links = list({
                            a["href"] for a in soup.find_all("a", href=True)
                            if "/en/detail/" in a["href"]
                        })
                        # Add the found links to the list of all URLs for the current province
                        all_urls.extend(links)
                        #print(f"[{p}] [{t}] Page {worker_id}: {len(links)} properties found")
                    else:
                        print(f"[{p}] [{t}] Page {worker_id} failed: {req.status_code}")

            tasks = [worker(i) for i in range(1, pages+1)]
            await asyncio.gather(*tasks)

            all_results[(p,t)] = all_urls
            print(f"Total properties for {t} in {p}: {len(all_urls)}")

    # Return the dictionary containing all property URLs categorized by province
    return all_results

def save_to_file(all_results, filename="all_properties.txt") -> None:
    """
    Method that saves the collected property URLs to a text file.

    :param all_results: Dictionary containing property URLs categorized by province, file name "all_properties.txt" by default.
    :return: A string indicating the total number of URLs saved and the name of the file.
    """
    with open(filename, "w") as f:
        for p, urls in all_results.items():
            for url in urls:
                f.write(url + "\n")

    total = sum(len(urls) for urls in all_results.values())
    print(f"All done! {total} URLs saved to {filename}")