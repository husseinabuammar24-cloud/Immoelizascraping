import requests
from dev.url_collection import provinces_url, save_to_file

def main() -> None:
    
    results = provinces_url ()       # 1. scrape all provinces
    save_to_file(results)              # 2. save to file


if __name__ == "__main__":
    main()