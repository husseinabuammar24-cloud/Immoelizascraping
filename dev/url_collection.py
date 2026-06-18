import time
import requests
from bs4 import BeautifulSoup

PROVINCES = [
    "Brussels", "Liège", "Vlaams-Brabant", "Namur", "Hainaut",
    "Brabant Wallon", "Limburg", "East Flanders", "Luxembourg",
    "West Flanders", "Antwerp"
]

TRANSACTIONS = ["rent", "sale"]


def provinces_url(provinces=PROVINCES, pages=50, delay=5, transactions=TRANSACTIONS) -> dict:
    """
    Method to collect property URLs for each province and page.

    :param provinces: List of provinces to scrape, default is 11 provinces in Belgium.
    :param pages: Number of pages to scrape for each province, default is 50.
    :param delay: Delay in seconds between requests to avoid overwhelming the server, default is 5 seconds.
    :param transactions: List of transaction types to scrape, default is ["rent", "sale"].
    :return: A dictionary containing property URLs categorized by province.
    """
    all_results = {}

    for t in transactions:
        # Only stop early on an empty page for "rent". "Sale" pages can return
        # a low/empty count mid-run (intermittent site/render issue) without
        # actually being the end of the listings, so for "sale" we always
        # scrape the full `pages` count regardless of empty pages in between.
        stop_on_empty = (t == "rent")

        for p in provinces:
            # Accumulate into the same set across both transaction types
            seen = all_results.setdefault(p, set())

            # Loop through each page for the current province
            for n in range(1, pages + 1):
                url = (
                    f"https://immovlan.be/en/real-estate?"
                    f"transactiontypes=for-{t}&propertytypes=house,apartment"
                    f"&provinces={p}&page={n}&noindex=1"
                )

                # Make the HTTP request with a user-agent header to avoid blocking
                req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

                # Check if the request was successful before parsing
                if req.status_code == 200:
                    soup = BeautifulSoup(req.text, "html.parser")
                    links = {
                        a["href"] for a in soup.find_all("a", href=True)
                        if "/en/detail/" in a["href"]
                    }

                    print(f"[{p}] [{t}] Page {n}: {len(links)} properties found")

                    # Actually add the found links to the running set
                    seen.update(links)

                    # For rent, stop early once a page is genuinely empty (end of listings).
                    # For sale, keep going through all `pages` even if a page is empty,
                    # since empty/partial pages can occur mid-run without meaning "the end".
                    if not links and stop_on_empty:
                        break
                else:
                    print(f"[{p}] [{t}] Page {n} failed: {req.status_code}")
                    break

                # Add a delay between requests to avoid overwhelming the server
                time.sleep(delay)

            print(f"\nTotal properties for {p} so far: {len(seen)}\n")

    return all_results


def save_to_file(all_results, filename="all_properties.txt") -> str:
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


if __name__ == "__main__":
    results = provinces_url()
    save_to_file(results)