# Immo-Eliza — Real Estate Data Collection

## Description
This project collects real estate data from immovlan.be, one of the most widely used property websites in Belgium. It works in two steps: first it gathers the URL of every listing across all Belgian provinces (11 provinces), then it visits each one and scrapes the property details — price, location, size, condition, and more.

As of 18 June 2026, around 14,000 property URLs have been collected, above the project target of 10,000 listings.

The result is a structured dataset built to train a machine-learning model that predicts property prices. This scraper is the first step of that larger project: it produces the raw data the model will later learn from.

## Repo Architecture & Git Flow

```
Immoelizascraping/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── Description about the dataset
└── dev/
|   ├──__init__.py
|   ├── url_collection.py
|   └── html_scraper.py
└── data/
    ├── all_properties.txt
    └── propertyData.csv
```

## How it works (project structure)
The scraper runs as one pipeline, launched by `main.py`:
- `url_collection.py` — Collects all the urls from the website (50 pages, 20 postings per page for one province)
- `html_scraper.py` — scraped the information about each property
- `main.py` — executes the all fuctions
- `all_properties_170626.txt` — is the file all the 14000 urls stored
- `Description_about_the_dataset` — the dataset information needed to be scraped

## Installation
Packages installed can be found in requirements.txt file.

## Usage

1. Clone the Repository to your local machine. 
2. to run the script, you can execute the main.py file from your command line. 
```
python main.py 
```
3. This script runs the whole code and it produces csv or json file with the all the links and scraped data. The code runs approc 3 hours. The final result is stored in propertyData.csv file of propertyData.json file in the main directory.

## Dataset
Description about the dataset file has the 28 columns of the data information needed that listed below: 

Data set and Data Type  
key [type] : description (unit)  
1.	transaction_type [category : "Rent", "Sale"] : Transaction type : to rent or for sale
2.	price [int] : Price (€)
3.	province [category : "Antwerp", "Brabant wallon", "Brussels", "Hainaut", "Liège", "Limburg", "Luxembourg", "Namur", "Oost vlaanderen", "Vlaams brabant", "West vlaanderen"]  : Province
4.	property_type [category : "Apartment", "House"] : Property type
5.	property_subtype [category : "Duplex", "Triplex", "Flat", "flatstudio", "groundfloor", "Penthouse", "House", "mixedbuilding", "Villa", "masterhouse"] : Property sub type
6.	date_of construction [int] : Date of construction
7.	property_condition [category : "New", "Normal", "Excellent", "To renovate", "Fully renovated"] : Property condition
8.	land_surface [int] : Surface of the land (m²)
9.	livable_surface [int] : Surface of the house (m²)
10.	energy_consumption [int] : Yearly total primary energy consumption (kwh/year)
11.	number_of_bedrooms [int] : Numbr of bedrooms
12.	number_of_bathrooms [int] : Number of bathrooms
13.	garage [int] : Number of garages
14.	elevator [bool] : Elevator or not
15.	swimming_pool [bool] : Swimming pool or not
16.	balcony [bool] : Balcony or not
17.	garden [int] : Garden surface (m²)
18.	terrace [int] : Terrasse surface (m²)
19.	furnished [bool] : Furnished or not
20.	postal_code [int] : Postal code
21.	street [string] : Street name
22.	street_number [int] : Street number
23.	availability [date] : Availability
24.	seller_id [int] : Id of the agency or 0 for private owners
25.	email [string] : Contact email
26.	phone_number [bool] : Phone number or not
27.	latitude [float] : Latitude geographic coordinate
28.	longitude [float] : Longitude geographic coordinate

## Visuals
Architecture diagram from your slides + a screenshot of the output CSV.

## Contributors
Ibrahim Ouezghar - Project Lead  
Gaetan Bricteux - QA & Data Architect  
Hussain Abuammar - Git Command  
Gunay Bayramova - Documentation

## Timeline
5-day team project — 12.06.2026-18.06.2026

## Sources
immovlan.be
