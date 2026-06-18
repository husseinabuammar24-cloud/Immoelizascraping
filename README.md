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
Description about the dataset file has the 24 columns of the data information needed that listed below: 

Title : Output final 
1.	Transaction Type (to rent or to sale)
2.	Furnished or not
3.	Property Type (Apartment, House, Businesses, Land, Garage, Investment property, Student housing, Miscellaneous property) 
4.	Date of construction 
5.	Condition (new or renovated or to renovated)
6.	Size of the land (m2)
7.	Size of the house (m2)
8.	PEB (kW for m²)
9.	Elevator or not? 
10.	Room numbers
11.	Numbers of bathroom
12.	Swimming or not?
13.	Balcon or not?
14.	Garden or not? 
15.	Terrasse or not?
16.	Price (€)
17.	region
18.	code postal 
19.	street
20.	nbr adress 
21.	Availability (datum) 
22.	Name agency or Private owner 
23.	Email
24.	Phone number (+32 ... or 02 ...) or not

## Visuals
Architecture diagram from your slides + a screenshot of the output CSV.

## Contributors
Ibrahim Ouezghar - Project Lead
Geaten Gbricteux - QA & Data Architect
Hussain Abuammar - Git Command
Gunay Bayramova - Documentation

## Timeline
5-day team project — 12.06.2026-18.06.2026

## Sources
immovlan.be