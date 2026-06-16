import time
import requests
from bs4 import BeautifulSoup

PROVINCES = [
    "Brussels", "Liège", "Vlaams-Brabant", "Namur", "Hainaut",
    "Brabant Wallon", "Limburg", "East Flanders", "Luxembourg",
    "West Flanders", "Antwerp"
]

def provinces_url(provinces=PROVINCES, pages=50, delay=5):
    all_results = {}

    for p in provinces:
        all_urls = []

        for n in range(1, pages + 1):
            url = (
                f"https://immovlan.be/en/real-estate?"
                f"transactiontypes=for-sale&propertytypes=house,apartment"
                f"&provinces={p}&page={n}&noindex=1"
            )
            req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                links = list({
                    a["href"] for a in soup.find_all("a", href=True)
                    if "/en/detail/" in a["href"]
                })
                all_urls.extend(links)
                print(f"[{p}] Page {n}: {len(links)} properties found")
            else:
                print(f"[{p}] Page {n} failed: {req.status_code}")
                break

            time.sleep(delay)

        all_results[p] = all_urls
        print(f"\nTotal properties for {p}: {len(all_urls)}\n")

    return all_results

def save_to_file(all_results, filename="all_properties.txt"):
    with open(filename, "w") as f:
        for p, urls in all_results.items():
            for url in urls:
                f.write(url + "\n")

    total = sum(len(urls) for urls in all_results.values())
    print(f"All done! {total} URLs saved to {filename}")

if __name__ == "__main__":
    results = provinces_url()
    save_to_file(results)