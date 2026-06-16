import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

class ImmoVlanScraper:
    """
    Class that can download and parse HTML page from ImmoVlan
    """
    def __init__(self, session : Session = Session()) -> None:
        """
        Constructor that creates a scraper with a session.

        :param session: Requests session to query the html page.
        """
        self.session = session

    def fetch_html(self, url: str) -> str:
        print("FETCHING:", url)

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = self.session.get(url, headers=headers, timeout=10)

            print("STATUS CODE:", response.status_code)

            return response.text

        except Exception as e:
            print("FETCH ERROR:", e)
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        Method that cleans a text by stripping out unwanted characters, whitespace.
        
        :param text: A string with the text to clean.
        :return: A string with the cleaned text.
        """
        text = text.strip() # remove end of line at the end of the text
        text = re.sub(r'\s+',' ',text) # replace no-break spaces
        return text
    
    def get_province_from_zip(self, zip_code):
        try:
            zip_code = int(zip_code)
        except:
            return "Inconnu"

        if 1000 <= zip_code <= 1299:
            return "Bruxelles"
        elif 1300 <= zip_code <= 1499:
            return "Brabant wallon"
        elif 1500 <= zip_code <= 1999 or 3000 <= zip_code <= 3499:
            return "Brabant flamand"
        elif 2000 <= zip_code <= 2999:
            return "Anvers"
        elif 3500 <= zip_code <= 3999:
            return "Limbourg"
        elif 4000 <= zip_code <= 4999:
            return "Liège"
        elif 5000 <= zip_code <= 5999:
            return "Namur"
        elif 6000 <= zip_code <= 6599 or 7000 <= zip_code <= 7999:
            return "Hainaut"
        elif 6600 <= zip_code <= 6999:
            return "Luxembourg"
        elif 8000 <= zip_code <= 8999:
            return "Flandre occidentale"
        elif 9000 <= zip_code <= 9999:
            return "Flandre orientale"
        else:
            return "Inconnu"

    def get_data(self, html: str) -> dict:
        """
        Method that parses the html, finds the required data, and returns it in a dictionary.
        
        :param html: A string with the html.
        :return: A dictionary with the required data.
        """
        data = {}
        soup = BeautifulSoup(html, "html.parser")

        # retrieve data (transactionType, propertyType, propertySubType, price, sellerType, sellerId, 
        #                zipCode, city, peb, newconstruction) from js script
        scripts = soup.find_all("script")
        for script in scripts:
            match = re.search(r'JSON\.stringify\(\{(.*?)\}\)', script.text, re.DOTALL)
            if match :
                json_str = '{' + match.group(1) + '}'
                # set keys between quotes
                json_str = re.sub(r'(\w+):', r'"\1":', json_str)
                # replace non quoted values
                json_str = re.sub(r': ([a-zA-Z]+)([,}])', r': "\1"\2', json_str)
                # replace single quotes by double quotes
                json_str = json_str.replace("'", '"')
                property_data = json.loads(json_str)
                # remove not required data
                for data in ["reference","transactionTypeId","propertyTypeId","propertySubTypeId", \
                             "id","vlanCode","sellerTypes","sellerId","priceRangeId","country","countryId"]:
                    property_data.pop(data)

                zip_code = property_data.get("zipCode") or property_data.get("zipcode")
                property_data["province"] = self.get_province_from_zip(zip_code)

                agency = self.get_agency(html)
                property_data["agency_name"] = agency.get("name")
                property_data["agency_phone"] = agency.get("phone")
                property_data["agency_url"] = agency.get("agency_url")
                return property_data
            
        return data
    
    def get_agency(self, html):

        print(">>> GET_AGENCY START")
        soup = BeautifulSoup(html, "html.parser")

        data = {
            "name": None,
            "phone": [],
            "email": [],
            "agency_url": None
        }

        # -------------------------
        # 1. seller_id
        # -------------------------
        match = re.search(r"seller_id['\"]?\s*:\s*['\"]?(\d+)", html)
        seller_id = match.group(1) if match else None

        print("SELLER_ID =", seller_id)

        if not seller_id:
            return data

        agency_url = f"https://immovlan.be/fr/guideimmobilier/detail/{seller_id}"
        data["agency_url"] = agency_url

        print("AGENCY URL =", agency_url)
        agency_html = self.fetch_html(agency_url)
        print("AGENCY HTML SIZE =", len(agency_html))

        # -------------------------
        # 2. find agency url (SAME AS WORKING CODE)
        # -------------------------
        
        agency_url = None

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "guideimmobilier/detail" in href and seller_id and seller_id in href:
                agency_url = urljoin("https://immovlan.be", href)
                break

        if not agency_url:
            return data

        data["agency_url"] = agency_url

        print("AGENCY URL =", agency_url)

        # -------------------------
        # 3. scrape agency page
        # -------------------------
        agency_html = self.fetch_html(agency_url)
        print("AGENCY HTML LENGTH =", len(agency_html))

        print("AGENCY HTML SIZE =", len(agency_html))
        print("AGENCY HTML START =", agency_html[:200])

        if "<!DOCTYPE html>" in agency_html and len(agency_html) < 2000:
            print("WARNING: page agency incomplete or blocked")
            return data
        agency_soup = BeautifulSoup(agency_html, "html.parser")
        print("H1 FOUND:", [h.get_text(strip=True) for h in agency_soup.find_all("h1")])
        print("AGENCY HTML START : ", agency_html[:200])
        title = agency_soup.find("h1")

        if not title:
            title = agency_soup.select_one("[class*='agency'], [class*='pro-user']")

        if title :
            data["name"] = self.clean_text(title.get_text())

        data["phone"] = re.findall(r"\+32\s?\d[\d\s./-]{6,}", agency_html)
        data["email"] = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", agency_html)

        return data


    @staticmethod
    def to_json_file(filepath: str, dictionary : dict) -> None :
        """
        Method that stores the data structure into a JSON file.

        :param filepath: A string with the file path where the json is stored.
        :param dictionary: A dictionary that is stored in the json file.
        """
        with open(filepath,"w") as file:
            json.dump(dictionary, file, ensure_ascii=False)

print("SCRIPT STARTED")