# Craigslist Cars Interactive Web App

This web application utilizes a custom-made csv file to analyze roughly 1,700,000 entries scraped from Craigslist cars and trucks data.

**You can find a [demo](https://ahmadosman.com/BestCarDeal/#flask-app) of this web app [here](https://ahmadosman.com/BestCarDeal/#flask-app)**

## Run the Web App

* Download the csv [here](http://knuth.luther.edu/~osmaah02/cars.csv)
* Clone this repo
* `python3.6 -m venv venv`
* `source venv/bin/active`
* You might want to update pip using `python-3.6 -m pip --upgrade pip`
* Install requirements with `python3.6 -m pip install -r requirements.txt`
* `python3.6 app.py`

## What's in the Data?

cars.csv contains the following columns:

* Listing URL (unique)

* Craigslist Region (categorical)

* Price (integer)

* Year (integer)

* Manufacturer (categorical)

* Make/Model (string)

* Condition (categorical)

* Cylinders (categorical)

* Fuel (categorical)

* Odometer (integer)

* Title Status (categorical)

* Transmission (categorical)

* Vehicle Identification Number (string)

* Drive (categorical)

* Size (categorical)

* Type (categorical)

* Color (categorical)

* Image URL (unique)

* State (categorical)

* County (categorical)

* Average Location Temperature (integer)

Users are not required to fill out every possible category when listing their vehicle, so this dataset contains holes in every column except for Listing URL, Craigslist Region and Price. Year contains a negligible amount of blank entries (less than .01%)

## Contributors

Designed by Ahmad Osman, Austin Reese, and Simon Parris
