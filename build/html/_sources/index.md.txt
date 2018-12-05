# Used Cars for Sale in the United States

## Our Motivation

Buying a car is never an easy task, especially when buying a used one. So many different factors go into determining the price of a vehicle that it's difficult to accurately predict what one should be paying. Aside from this there are some parts of the country where used car sales are few and far between and the prices are not so desirable. Using our dataset of used car sales we aimed to clarify some of these unknown variables and provide an easier experience for those searching for a car. Our goal was not to simply create static visualizations that compared cars from winter 2018, but instead we aim to create an application of sorts that allows users to continuously update the vehicles in their search.

## The Dataset

Our dataset contains 1.7 million used vehicle sales from Craigslist.org

The columns are as follows:

* **url** - Unique - *Listing URL*
* **city** - String - *Given Craigslist region*
* **price** - Integer - *Listing price*
* **year** - Integer - *Year of manufacturing*
* **manufacturer** - String - *Manufacturing company*
* **make** - String - *Model of vehicle*
* **condition** - String - *Condition of vehicle*
* **cylinders** - String - *Number of cylinders*
* **fuel** - String - *Type of fuel required*
* **odometer** - Integer - *Miles traveled*
* **title_status** - String - *Vehicle title status/existance*
* **transmission** - String - *Transmission of vehicle*
* **drive** - String - *Drive of vehicle*
* **size** - String - *Size of vehicle*
* **type** - String - *Type of vehicle*
* **paint_color** - String - *Color of vehicle*
* **image_url** - String - *Image URL*
* **latitude** - Integer - *Latitude of listing*
* **longitude** - Integer - *Longitude of listing*
* **county_name** - String - *Name of County in which listing is located*
* **county_fips** - Integer - *County of listing's Federal Information Processing Standards code*
* **state_code** - String - *Name of state in which listing is located*
* **state_name** - String - *2 letter state abbreviation*
* **state_fips** - Integer - *State of listing's Federal Information Processing Standards code*
* **weather** - Integer - *Average historical temperature of listing's location between October and November*

### Initial Creation

We deployed a scraper which utilized python and requestsHTML to take every used car for sale from every North American Craigslist website. Regions were located by continuously following *Nearby CL* links until no unexplored websited remained.

![craigs3.png](img/craigs3.png)

Following the cars+trucks link takes us to the following page.

![craigs1.png](img/craigs1.png)

The price and image url were pulled from the search page, while the rest of the variables were pulled from the main listing page.

![craigs2.png](img/craigs2.png)

Latitude/Longitude was pulled from a specific tag on the Google Maps object, and the rest were pulled from the variables below. Not all variables were listed with every vehicle, so some rows contain blank values. 

The program loops through every listing on the search page then continues looping through the search pages (e.g. the next button at the bottom of search results) until there are no more results. Once the end is reached the program moves on to the next untapped region and restarts this process, continuing until all regions have been explored.

### Secondary Data Gathering

## Basic Exploration

## Big Questions

## Further Exploration

## Flask App

## World Happiness Index

## What's Next?
