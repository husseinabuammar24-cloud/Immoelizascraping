# Immo-Eliza — Real Estate Data Collection

## Description
This project collects real estate data from immovlan.be, one of the most widely used property websites in Belgium. It works in two steps: first it gathers the URL of every listing across all Belgian provinces (11 provinces), then it visits each one and scrapes the property details — price, location, size, condition, and more.

As of 18 June 2026, around 14,000 property URLs have been collected, above the project target of 10,000 listings.

The result is a structured dataset built to train a machine-learning model that predicts property prices. This scraper is the first step of that larger project: it produces the raw data the model will later learn from.

## Repo Architecture & Git Flow

Immoelizascraping/

├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── Description about the dataset
└── dev/
    ├──__init__.py
    ├── url_collection.py
    └── html_scraper.pyy

## How it works (project structure)
The scraper runs as one pipeline, launched by `main.py`:
- `url_collection.py` — Collects all the urls from the website (50 pages, 20 postings per page for one province)
- `html_scraper.py` — scraped the information about each property
- `main.py` — executes the all fuctions
- `all_properties_170626.txt` — is the file all the 14000 urls stored
- `Description_about_the_dataset` — the dataset information needed to be scraped

## Installation
Packages installed can be found in requirements.txt file

## Usage

1. Clone the Repository to your local machine. 
2. to run the script, you can execute the main.py file from your command line. 

Python main.py 

3. This script runs the whole code and it produces json file with the all the links and scraped information. The code runs approc 3 hours. the final result is .csv format in your directory

## Dataset
Description about the dataset file has the 28 columns of the data information needed that listed below: 

Data set and Data Type 
-----------------------
key [type] : description (unit)
-----------------------
1.	Transaction_type [category : "Rent", "Sale"] : Transaction type : to rent or for sale
2.	Price [int] : Price (€)
3.	Province [category : "Antwerp", "Brabant wallon", "Brussels", "Hainaut", "Liège", "Limburg", "Luxembourg", "Namur", "Oost vlaanderen", "Vlaams brabant", "West vlaanderen"]  : Province
4.	Property_type [category : "Apartment", "House"] : Property type
5.	Property_subtype [category : "Duplex", "Triplex", "Flat", "flatstudio", "groundfloor", "Penthouse", "House", "mixedbuilding", "Villa", "masterhouse"] : Property sub type
6.	Date_of construction [int] : Date of construction
7.	Property_condition [category : "New", "Normal", "Excellent", "To renovate", "Fully renovated"] : Property condition
8.	Land_surface [int] : Surface of the land (m²)
9.	Livable_surface [int] : Surface of the house (m²)
10.	Energy_consumption [int] : Yearly total primary energy consumption (kwh/year)
11.	Number_of_bedrooms [int] : Numbr of bedrooms
12.	Number_of_bathrooms [int] : Number of bathrooms
13.	Garage [int] : Number of garages
14.	Elevator [bool] : Elevator or not
15.	Swimming_pool [bool] : Swimming pool or not
16.	Balcony [bool] : Balcony or not
17.	Garden [int] : Garden surface (m²)
18.	Terrace [int] : Terrasse surface (m²)
19.	Furnished [bool] : Furnished or not
20.	Postal_code [int] : Postal code
21.	Street [string] : Street name
22.	Street_number [int] : Street number
23.	Availability [date] : Availability
24.	Seller_id [int] : Id of the agency or 0 for private owners
25.	Email [string] : Contact email
26.	Phone_number [bool] : Phone number or not
27.	Latitude [float] : Latitude geographic coordinate
28.	Longitude [float] : Longitude geographic coordinate

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
