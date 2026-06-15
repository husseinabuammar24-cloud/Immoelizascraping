import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import re

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

    def fetch_html(self, url : str) -> str:
        """
        Method that requests raw HTML text.

        :param url: A string with the url of the html to request.
        :return: A string with the html text.
        """
        try:
            # header is used to tell the website that the script is not from automated bot
            headers = {"User-Agent":"Mozilla/5.0"}
            response = self.session.get(url, headers = headers)
            return response.text
        except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout) as err:
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
                return property_data
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
