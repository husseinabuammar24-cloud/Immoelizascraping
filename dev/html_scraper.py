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
        """
        Method that requests raw HTML text. 

        :param url : A string with the url of the html to request. 
        : return: A string with the html text. 

        """
        try:
            # header is used to tell the website that the script is not from automated bot 
            headers = {"User-Agent": "Mozilla/5.0"}
            response = self.session.get(url, headers=headers)

            return response.text

        except (requests.exceptions.HTTPError,requests.exceptions.ReadTimeout) as err:
            print(err.args[0])
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
    
    def get_province_from_zip(self, zip_code) -> str:
        try:
            zip_code = int(zip_code)
        except:
            return "Unknown"

        if 1000 <= zip_code <= 1299:
            return "Brussels"
        elif 1300 <= zip_code <= 1499:
            return "Brabant wallon"
        elif 1500 <= zip_code <= 1999 or 3000 <= zip_code <= 3499:
            return "Vlaams brabant"
        elif 2000 <= zip_code <= 2999:
            return "Antwerp"
        elif 3500 <= zip_code <= 3999:
            return "Limburg"
        elif 4000 <= zip_code <= 4999:
            return "Liège"
        elif 5000 <= zip_code <= 5999:
            return "Namur"
        elif 6000 <= zip_code <= 6599 or 7000 <= zip_code <= 7999:
            return "Hainaut"
        elif 6600 <= zip_code <= 6999:
            return "Luxembourg"
        elif 8000 <= zip_code <= 8999:
            return "West vlaanderen"
        elif 9000 <= zip_code <= 9999:
            return "Oost vlaanderen"
        else:
            return "Unknown"

    def get_data(self, html: str) -> dict:
        """
        Method that parses the html, finds the required data, and returns it in a dictionary.
        
        :param html: A string with the html.
        :return: A dictionary with the required data.
        """
        data = {}
        soup = BeautifulSoup(html, "html.parser")

        # Handle error 404 page if property page does not exist
        titles = soup.find_all("title")
        for title in titles:
            if title.text == "Http404":
                return data

        # retrieve data (transaction_type, price, property_type, seller_type, postal_code) from js script
        scripts = soup.find_all("script")
        for script in scripts:
            match = re.search(r'window.AD_LONGITUDE = \'(.*?)\';\n\s+window.AD_LATITUDE = \'(.*?)\';\n', script.text)
            if match :
                longitude = match.group(1)
                latitude = match.group(2)
                data["longitude"] = float(longitude)
                data["latitude"] = float(latitude)
            match = re.search(r'STORAGE_KEY_PROPERTY_DETAILS,\n\s+JSON\.stringify\(\{(.*?)\}\)', script.text, re.DOTALL)
            if match :
                json_str = '{' + match.group(1) + '}'
                # set keys between quotes
                json_str = re.sub(r'(\w+):', r'"\1":', json_str)
                # replace non quoted values
                json_str = re.sub(r': ([a-zA-Z]+)([,}])', r': "\1"\2', json_str)
                # replace single quotes by double quotes
                json_str = json_str.replace("'", '"')
                property_data = json.loads(json_str)
                if "transactionType" in property_data:
                    data["transaction_type"] = property_data["transactionType"]
                if "price" in property_data:
                    data["price"] = int(float(property_data["price"].replace(",",".")))
                if "propertyType" in property_data:
                    data["property_type"] = property_data["propertyType"]
                if "propertySubType" in property_data:
                    data["property_subtype"] = property_data["propertySubType"]
                if "sellerType" in property_data and "sellerId" in property_data:
                    data["seller_id"] = property_data["sellerId"] if property_data["sellerType"] == "estateAgents" else 0
                if "zipCode" in property_data:
                    data["postal_code"] = int(property_data["zipCode"])

        # retrieve data from general info division
        gen_data = {}
        data_divs = soup.find_all("div", class_="data-row-wrapper")
        for data_div in data_divs:
            h4_elems = data_div.find_all("h4")
            for h4 in h4_elems:
                key = h4.text.strip()
                p = h4.find_next('p')
                if p:
                    gen_data[key] = p.text.strip()
        if "Build Year" in gen_data:
            data["date_of_construction"] = int(gen_data["Build Year"])
        if "State of the property" in gen_data:
            data["property_condition"] = gen_data["State of the property"]
        if "Total land surface" in gen_data:
            data["land_surface"] = int(gen_data["Total land surface"].split(" ")[0])
        if "Livable surface" in gen_data:
            data["livable_surface"] = int(gen_data["Livable surface"].split(" ")[0])
        if "Yearly total primary energy consumption" in gen_data:
            data["energy_consumption"] = int(gen_data["Yearly total primary energy consumption"].split(" ")[0])
        if "Number of bedrooms" in gen_data:
            data["number_of_bedrooms"] = int(gen_data["Number of bedrooms"])
        if "Number of bathrooms" in gen_data:
            data["number_of_bathrooms"] = int(gen_data["Number of bathrooms"])
        if "Number of garages" in gen_data:
            data["number_of_garage"] = int(gen_data["Number of garages"])
        if "Elevator" in gen_data:
            data["elevator"] = gen_data["Elevator"] == "Yes"
        if "Swimming pool" in gen_data:
            data["swimming_pool"] = gen_data["Swimming pool"] == "Yes"
        if "Balcony" in gen_data:
            data["balcony"] = gen_data["Balcony"] == "Yes"
        if "Surface garden" in gen_data:
            data["garden"] = int(gen_data["Surface garden"].split(" ")[0])
        if "Surface terrace" in gen_data:
            data["terrace"] = int(gen_data["Surface terrace"].split(" ")[0])
        if "Furnished" in gen_data:
            data["furnished"] = gen_data["Furnished"] == "Yes"
        if "Availability" in gen_data:
            data["availability"] = gen_data["Availability"]
        
        zip_code = data.get("postal_code")
        province = self.get_province_from_zip(zip_code)
        if province != "Unknown":
            data["province"] = province

        street, house_number = self.get_address(soup)
        if street is not None:
            data["street"] = street
        if house_number is not None:
            data["house_number"] = house_number

        agency = self.get_agency(html)
        if "email" in agency and agency["email"] != "":
            data["email"] = agency.get("email")
        if "phone" in agency and agency["phone"] != "":
            data["phone_number"] = agency["phone"]

        return data
    
    def get_agency(self, html) -> dict :

        """
            Method that extracts agency information (name, phone, email, agency URL)
            from the property HTML page.

            :param html: Raw HTML of the property page.
            :return: Dictionary containing agency data:
                    - name (str): Agency name
                    - phone (list): List of phone numbers
                    - email (list): List of email addresses
                    - agency_url (str): URL of the agency page
        """

        soup = BeautifulSoup(html, "html.parser")

        data = {
            "name": "",
            "phone": "",
            "email": "",
            "agency_url": ""
        }

        # 1. Extract seller_id from the property page HTML
        match = re.search(r"seller_id['\"]?\s*:\s*['\"]?(\d+)", html)
        seller_id = match.group(1) if match else None

        if not seller_id:
            return data

        agency_url = f"https://immovlan.be/fr/guideimmobilier/detail/{seller_id}"
        data["agency_url"] = agency_url

        agency_html = self.fetch_html(agency_url)

        # 2. Find the agency URL from the property page links
        
        agency_url = None

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "guideimmobilier/detail" in href and seller_id and seller_id in href:
                agency_url = urljoin("https://immovlan.be", href)
                break

        if not agency_url:
            return data

        data["agency_url"] = agency_url
        
        "3.scrape agency page"

        agency_html = self.fetch_html(agency_url)

        if "<!DOCTYPE html>" in agency_html and len(agency_html) < 2000:
            print("WARNING: page agency incomplete or blocked")
            return data
        agency_soup = BeautifulSoup(agency_html, "html.parser")
        title = agency_soup.find("h1")

        if not title:
            title = agency_soup.select_one("[class*='agency'], [class*='pro-user']")

        if title :
            data["name"] = self.clean_text(title.get_text())

        data["phone"] = str(re.findall(r"\+32\s?\d[\d\s./-]{6,}", agency_html))
        data["email"] = str(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", agency_html))

        return data
    
    def get_address(self, soup:BeautifulSoup)->tuple[str|None,int|None]:

        """:
        Method that extracts the street name and house number from the property page title
        :param soup: A BeautifulSoup object containing the parsed HTML page.
        :return: A tuple containing:
                - street (str | None): The street name.
                - house_number (int | None): The house number.
        """

        if not soup.title:
            return None, None

        title = soup.title.text

        try:

            keywords = [
                "for sale in",
                "for rent in"
            ]

            address_part = None

            for keyword in keywords:
                if keyword in title:
                    address_part = title.split(keyword)[1]
                    break

            if address_part is None:
                return None, None

            address_part = address_part.split("(")[0].strip()

            match = re.search(r"(.+?)\s+(\d+)", address_part)

            if match:
                street = match.group(1).strip()
                house_number = int(match.group(2))
                return street, house_number

            return address_part, None

        except Exception:
            return None, None

    @staticmethod
    def to_json_file(filepath: str, dictionary : dict) -> None :
        """
        Method that stores the data structure into a JSON file.

        :param filepath: A string with the file path where the json is stored.
        :param dictionary: A dictionary that is stored in the json file.
        """
        with open(filepath,"w") as file:
            json.dump(dictionary, file, ensure_ascii=False)