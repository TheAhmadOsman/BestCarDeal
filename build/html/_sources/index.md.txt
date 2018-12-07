# <center> Used Cars for Sale in the United States </center>
<center>Ahmad Osman, Austin Reese, and Simon Parris</center>

## Our Motivation
---

Buying a car is never an easy task, especially when buying a used one. So many different factors go into determining the price of a vehicle that it's difficult to accurately predict what one should be paying. Aside from this there are some parts of the country where used car sales are few and far between and the prices are not so desirable. Using our dataset of used car sales we aimed to clarify some of these unknown variables and provide an easier experience for those searching for a car. Our goal was not to simply create static visualizations that compared cars from winter 2018, but instead we aim to create an application of sorts that allows users to continuously update the vehicles in their search.

## The Dataset
---
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
* **title_status** - String - *Vehicle title status/existence*
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

## Initial Creation
---

We deployed a scraper which utilized python and requestsHTML to take every used car for sale from every North American Craigslist website. Regions were located by continuously following *Nearby CL* links until no unexplored website remained.

![craigs3.png](img/craigs3.png)

Following the cars+trucks link takes us to the following page.

![craigs1.png](img/craigs1.png)

The price and image url were pulled from the search page, while the rest of the variables were pulled from the main listing page.

![craigs2.png](img/craigs2.png)

Latitude/Longitude was pulled from a specific tag on the Google Maps object, and the rest were pulled from the variables below. Not all variables were listed with every vehicle, so some rows contain blank values. 

The program loops through every listing on the search page then continues looping through the search pages (e.g. the next button at the bottom of search results) until there are no more results. Once the end is reached the program moves on to the next untapped region and restarts this process, continuing until all regions have been explored.

## Secondary Data Gathering
---
The data we have gathered so far seems very promising for exploration, however, we feel like it should be more grounded, literally. We wanted to connect each car being sold on Craigslist to a State and even a County. This would help us in our visualization and might give us some insights in our analysis.

Before we look into how to bring the geographical data, we need to decide whether we think we should only use our initial 700,000 entries taken by the end of October, or to incorporate more recent entries from Craigslist that we were able to scrape at the beginning of November. After some thinking, we've decided that it would not hurt to merge the data we've gathered between October and November. We started with 700,000 entries of vehicles being sold by late October and expanded to 1,700,000 by early November. However, this is not going to be an easy task.


### Merging Data
We need to find out a way to merge the data, and to remove any duplicates that might had been on the website when we started our initial data collection and was still live on Craigslist by the time we did our second scraping. Furthermore, we did not want to keep working on the data in its CSV format, but rather use SQL for and have a Database on disk until we're done with our data collection. We decided that the data can be saved as a db format using sqlite, and that we would make URL column a primary key since it is a unique field. Having the URL as a primary key helped us merge the data we scrapped in October and November without any duplicates. Alas, we have 1.7 million vehicles in our dataset.


### Finding Geographical Information
As we begin, we assumed that our data having longitudes and latitudes would make this quest an easy one, but such is life. First, we have to understand that our data at this point is very big, and that a simple API would not let us make 1.7 million calls, and then we have to also know that sqlite does not support concurrent tasks and would only allow one entry to be updated per database. 

We tried searching for any database that would provide us the State and the Country given that we pass in longitude and latitude, but all our efforts were not successful. At one point, we almost gave up on this task, especially that the kind of providers we could find were either unreliable or quite expensive.

Fortunately, we came across a Federal website that among the data they'd provide you given a longitude and a latitude were what we have been looking for. The [Federal Communications Commission Area API](https://geo.fcc.gov/api/census/#!/area/get_area) allowed us to send in a longitude and latitude, and to get the following data:
* county_name
* county_fips
* state_code
* state_name
* state_fips

If you think about it, this is an awesome tool provided by the American Government, and the fact that we were able to not only collect the relative data of 1,700,000 entries but also to do that in under 2 hours is even more impressive. Long story short, we implemented a multi-threaded program that made about 15,000 requests per minute. We also had to migrate from Sqlite to PostgreSQL, since the former did not have any multi-threading support.

All in all, we were able to to get the geographical data we wanted for 1,700,000 entries, and not only to that for this huge amount of data, but to also do it within two hours, which seemed impossible when we started. We had some failed responses but that is because the sent longitudes and latitudes belonged to Canada, and this failed responses helped us get rid of any entries outside of the United States.


### Weather Data
Also, we were interested in seeing whether weather might have an influence on the data. Also, after taking Prof. Lee, he alerted us that some people might be selling their cars because of floods, and we wanted to keep such idea in our minds for possible further exploration.

Unfortunately, to collect specific data, such as floods at specific counties during specific dates, that would've required us to spend thousands of dollars on services that provide such information. Our only hope was to find a governmental data to help us with our data collection. We found [US Climate Data](https://www.usclimatedata.com/climate/alabama/united-states/3170) website that had historical weather data for each State. We decides that this might be a long shot but we got the average historical temperature for October and November for each state and incorporated that in our dataset.

## Big Questions
---

### What is the Best Deal on a Used Car?

To find the best possible deal on an used car, we must first take into consideration the general preferences of the average person looking to buy a vehicle. Therefore, in exploring the dataset, we will use 5 categories to find the best type of vehicles available for purchase, in order to find the best deals on a used car. The 5 categories include the vehicle's price, manufacturer, condition, state, and year. People who are less knowledgeable about vehicle specifications are more likely to explore these variables when buying a car. Most college students, like ourselves, will be looking for a used car with familiar manufacturers at a cheap price and in good condition. Other variables such as vehicle size will also be taken into consideration as customers will also need to consider what vehicle size is more suitable for them. 

We believe that finding a good car for any individual can take a tremendous amount of research, and that it usually can take a span of a month to two, and that was one of the reasons we wanted to do our analysis on the total amount of cars being sold on Craigslist over a month. We are assuming that 1.7 million cars would be what individuals looking to choose from in any given month, and our exploration is assuming that too.

We're dealing with 53 unique manufacturers, 6 unique conditions, and 4 car sizes plus 1834 counties and 51 states.

To reiterate, the five factors we are focusing on are:
* Price
* Manufacturer
* Condition
* State
* Year

## Basic Exploration
---
### The Distribution of the Top 10 Car Manufacturers
![manufacturers-chart](img/manufacturers-chart.png)
This is the percentage distribution of the cars being manufactured by the top 10 manufacturers.

![manufacturers-bar](img/manufacturers-bar.png)
This is the count of the cars being manufactured by the top 10 manufacturers.

Here we are looking to see the distribution of the top 10 manufacturing companies within the dataset. If you prefer Ford vehicles, Ford has the highest number of vehicles available for purchase, meaning you have a large number of vehicles to choose from, and also worry not as the laws of demand and supply will probably be in your favor. Ford is followed by Chevrolet and Toyota. BMW has the lowest number of cars available for sale, so persons who prefer this brand may have a lower chance of finding their ideal vehicle.

### The Distribution of the Top 10 States to Buy a Car in
![states-chart](img/states-chart.png)
This is the percentage distribution of the cars being sold in the top 10 states.

![states-bar](img/states-bar.png)
This is the count of the cars being sold in the top 10 states.

Here we are looking at the top 10 distribution of cars for sale by state. States such as California, with a population of approximately 34 million will generally have more vehicles available for purchase than other states. California has the highest number of vehicles for purchase with less than 160,000 vehicles for sale. States such as Washington will generally have less vehicles available for sale, with a population count of approximately 7 million. Washington has less than 60,000 vehicles available for purchase.

### Weather-Condition Correlation
![weather-vehicle-freq](img/weather-vehicle-freq.png)
In this graph, we are looking to see the correlations with weather and vehicle conditions, as this is another factor to consider when looking for a vehicle. Individuals looking to buy cars in excellent condition should aim for states generally which are generally between 55-60 degrees in temperature. It should be noted that weather does not have a major effect on the condition of cars for sale, as cars with poor conditions are sold within the similar temperature range are cars in excellent condition.

### Condition Distribution
![condition-count-bar](img/condition-count-bar.png)
This graph shows the number of vehicles within a specific condition. Vehicles in an excellent condition have the highest number with above 400,000 entries, followed by cars in good and like new condition. Vehicles that are salvaged have the least number of entries with less 25,000 vehicles available for sale. Persons will generally not want to post severely depreciated vehicles for sale, as they are low in value.

### Size Distribution
![size-count-bar](img/size-count-bar.png)
For individuals concerned about car size, this graph shows the number of vehicles for sale within a specific size. Individuals looking for full-sized vehicles will have over 300,000 entries to look at, whereas persons looking for sub-compact cars will have the least amount of entries to look at, with entries less than 50,000 entries.

### Average Price per Condition
![avgprice-condition-bar](img/avgprice-condition-bar.png)
The graph above shows the mean price for each condition. New vehicles have an average sales price of above $20,000, followed by vehicles which are _like new_, with an average sales price of above $15,000. Individuals looking for cheaper alternatives should look at vehicles with good to fair condition, as they will on average have to spend less than $10,000 for a vehicle. Vehicles with a fair or salvaged condition are most likely severely depreciated, suggesting their low average pricing of less than $5000.

### Average Price per State
![avgprice-state-bar](img/avgprice-state-bar.png)
The graph above shows the mean prices for vehicles within each state. Persons looking for cheap vehicles, will be more likely to look at states such as District of Columbia and Delaware, as they both have a mean average of less than $7,500 for cars available for sale. Hawaii has the highest mean cost of vehicles with over $20,000 and there are several factors that could suggest why vehicles are so costly in Hawaii. Some reasons for these could be a higher cost of living in Hawaii or more luxury vehicles are available for purchase in Hawaii.

### Average Price per Manufacturer
![avgprice-manufacturer-bar](img/avgprice-manufacturer-bar.png)
This graph shows the mean prices of vehicles for each manufacturer. Luxury vehicles such as ferrari, have a high average sales price of $80,000, followed by aston and aston-martin with average sales prices of less than $60,000. Ferraris and other luxury vehicles are often expensive because they are often built with expensive and high-quality materials and are manufactured to tailor to individuals looking for a high quality vehicle. Persons looking for cheaper alternatives can look to brands such as mercury and volkswagen, who have average sales prices of less than $5,000. Vehicles within this range are more suited for persons with lower budgets, who are more concerned about going from Point A to Point B.

## Further Exploration

### Scatter Plots
---

### Plotting Prices and Odometers

![scatter.png](img/scatter.png)

This scatter plots measures prices and odometers, while the shade of the dot represents its year. We can see a clearly defined fall in price as the odometer increases, and we can see that the year of manufacturing falls as the odometer increases/price decreases. The graph, however, is quite chaotic with a plethora of outliers. A graph like this would look far better as a line plot, and the sheer amount of data in our dataset doesn't really lend itself to plotting each individual entry in a plot.

### Violins
---

### Year Distribution by Condition

![yearConditionViolin.png](img/yearConditionViolin.png)

The graph above displays the frequency distributions for cars in the dataset of a certain condition. For individuals more concerned about the condition of their vehicles, they will be more likely to consider
cars of a new condition, as they would have a more recent year of manufacturing(between 2015-2018). Cars in poor/salvaged condition are most likely depreciated vehicles within the range of years 2000-2005. The graph clearly suggests that if you want a vehicle in a great condition, you should purchase a vehicle with a year of manufacturing closest to the most recent year.

* The white dot represents the median
* The thick gray bar in the center represents the interquartile range
* The thin gray line represents the 95% confidence interval
* On each side of the gray line is a kernel density estimation to show the distribution shape of the data. 
* Wider sections of the violin plot represent a higher probability that members of the population will take on the given value;
* The skinnier sections represent a lower probability.

### Price Distribution by Condition

![conditionViolins.png](img/conditionViolins.png)

This violin graph measure the correlation between the price of vehicles and their seller-assigned conditions. We can see a pretty obvious (and unsurprising) hierarchy of new, like new, excellent, good, fair, and salvage. One surprise, however, is the similarity in price between fair and salvage vehicles. This suggests that vehicles deemed "fair" on Craigslist are actually in quite poor condition and worth almost as much as a parts-only car.

### Line Graphs
---

### Mean/Median Price by Odometer

![odomPriceLines.png](img/odomPriceLines.png)

Here we measure the mean/median price as the odometer declines for each category of vehicle condition. We can see that the first four graphs are pretty similar (new, like new, good, and fair) with minor falls between each lesser category. Transitioning from good to fair, however, sees the price nearly bottom out. Clearly a "fair" distinction on Craigslist comes with a major decrease in vehicle quality.

### Heatmaps
---

### Heated by Number of Listings - 1990-2005

![1990-2005 Map](img/1990-2005.png)
[Interactive Version Here - Heated Map by Number of Listings - 1990-2005](1990-2005.html)

This map depicts car listings when they were manufactured between 1990 and 2005. This map is quite crowded and while it tells us a lot about the distribution of car listings across the United States, the 1990-2005 filter isn't very interesting.

### Heated by Number of Listings - 1990-1995

![1990-1995 Map](img/1990-1995.png)
[Interactive Version Here - Heated Map by Number of Listings - 1990-1995](1990-1995.html)

In an effort to narrow our results, lets change the filter to 1990-1995. This thins the map but the distribution is still the same. It does appear that there are substantially less listings in the western United States which could suggest that rural areas have newer cars, but numbers are thinned on the east side as well so it's difficult to draw any valid conclusions.

### Heated by Number of Listings - Toyotas

![Toyotas Map](img/toyotas.png)
[Interactive Version Here - Heated Map by Number of Listings - Toyotas](toyotas.html)

Perhaps a totally different filter will reveal something interesting. This is a map of Toyotas only, and there's actually something to see here. Toyotas are quite prevalent in urban areas but they're nearly extinct in rural ones. We can contribute this to Toyotas reputation for building smaller, cost efficient cars which aren't quite as desirable in rural areas.


### Heated by Number of Listings by County

![carsForSaleMap.png](img/carsForSaleMap.png)
[Interactive Version Here - Heated Map by Number of Listings by County](https://plot.ly/~reesau01/2)

This map displays the number of vehicles listed per county. Unsurprisingly, counties with high amounts of listings lie along the west/east coast, along with Flordia and metropolitan areas throughout the country (Denver, Chicago, Dallas, Minneapolis, etc.). The map also indicates that, with the exception of Denver and the west coast, the west side of the country is quite sparse when it comes to car listings. The east side of the United States contains far more sales.

### Heated by Average Price by County

![priceByCountyMap.png](img/priceByCountyMap.png)
[Interactive Version Here - Heated Map by Average Price by County](https://plot.ly/~reesau01/4)

This map graphs the average price of vehicles by county across the United States. One striking observation is the increase in vehicle cost in rural areas. The prices of cars in states such as Idaho, North/South Dakota, and Wyoming, and rural parts of the midwest are far more expensive than those in the Eastern half of the nation. Cars on the East Coast also cost a faire amount less than those on the West Coast, with the coast of California boasting some pretty high prices.

### Heated by Correlations

![squareHeatmap.png](/img/squareHeatmap.png)

All numeric variables' correlations are compared in this graph. Most variables aren't correlated at all, with the exception of moderate negative correlation between price and year, slight negative correlation between year and odometer, and slight positive correlation between year and price. We also see major negative correlation between weather and latitude which isn't surprising at the slightest for those who are familiar with the planet we live on.

### Quantile Tables
---

Lets say we're searching for a used car, but we have no idea what a fair price would be. Enter quantile tables. These tables aren't super eye-catching, but they're very practical tools for determining what we should be paying for a given car. They take two numeric values, and in this example I'll use odometer (miles the car has been driven) and price given that it's a very practical combination when searching for a decent used car. The x axis (columns) will be grouped by a range of odometers determined by percentiles. 0-10th percentile may be 0-25000 miles driven, 11-20 could be 25000-50000, etc. Once these groups are determined we slice the our dataframe into 10 separate frames according to which category they fall under (a car with 12500 miles will be in the first group while 45000 will be in the second). Finally, we find percentiles for the prices of cars within each group. This sounds somewhat complicated but the graphs are far easier to understand and resemble simple heatmaps.

### Grouped by Odometer - Means of Price
![all.png](img/all.png)

Above is a graph featuring the entire dataframe, sorted by odometer with means of price. For example, lets say we wanted to purchase a car with no more than 70000 miles on it. We can check out the fourth column (46000-69295) to get an estimate on what a good price would be. The first row tells us that the top 10% of deals have an average price of \$3207, which seems very affordable yet somewhat unrealistic. It would be wise to target a top 30% deal, which would mean that our car would cost less than $10048.

### Grouped by Odometer - Means of Price - Fords
![fords.png](img/fords.png)

The first graph is great but it's very broad and if we're looking to buy a specific car it's not going to help us very much. Above is a graph plotting the same odometer/price, only this time the data is taken from Fords only. We can see that Ford's are a little more expensive and have a tad more miles on them, but it's still not descriptive enough for us data scientists.

Grouped by Odometer - Means of Price - Fords in 'Good' Condition
![goodFords.png](img/goodFords.png)

As broke college students we are not looking for the greatest quality car, so this graph shows Fords with the 'Good' condition tag. Now we can see that a top 30% deal our 70000 mile car shouldn't cost any more than $6000, probably a little less. But still, a Ford in good condition isn't as descriptive as we'd like as it still applies to a plethora of vehicles.

Grouped by Odometer - Means of Price - Ford Midsize Sedans in 'Good' Condition
![goodFordMidsizeSedan.png](img/goodFordMidsizeSedan.png)

Finally, a chart specific enough to draw accurate conclusions from. This chart shows 'Good' mid-size sedans manufactured by Ford. We now see that the car that we once thought we should try to buy for less than \$10000 should be pursued for no more than $3000. Overall these quantile tables are an excellent way to determine an asking price for a used car, they're easily automatable (as displayed in the Flask app) and also easy to build by hand.

## Flask App
---

To help us browse the data early on (and because it's cool), we created a Flask app which allows users to create custom graphs displaying information relevant to them. This is the first step in our goal to create something that continues to be relevant beyond its creation. The app does not require any updates in its current form, all it needs to update automatically is a new dataset which can be created using a script that scrapes Craigslist.

Lets demo this in class: Color and Price Graphs.

Watch our demos with the links below!

![1.webm](videos/1.webm)
![2.webm](videos/2.webm)
![3.webm](videos/3.webm)
![4.webm](videos/4.webm)
![5.webm](videos/5.webm)

## What's Next
---

With some optimization, the data can be scraped lively from Craigslist and our other secondary sources, and then getting fed into our Flask app(this needs optimization too). What we are hoping to reach is to have a platform that would help you not only visualize data but also analyze the data and get to the specific entries of each graph/table/map you are looking at.

Imagine a platform, updated lively, that would allow you have the top 10%/15%/25% deals populating a Google Map of a specific State/County, and not that only, but to give your insights and statistics about the car manufacturer and its popularity, whether that top deal by milage is also a top deal by state or manufacturer.

We have come to the conclusion that this data have the ability to give insights about all of that and to help you make the right decision in finding yourself a car. Among the questions that we think this data can help us answer now or in further explorations:
* Whats a good deal on a used car?
* What is the best deal on a used car?
* Where should student go to purchase a car?
* Which state has the best deals on new/used cars?
* Where are the best deals on used cars in a specific state? (e.g Iowa)
* Does car colour affect item frequency/sales price?
* Does weather have an effect on conditions?
* Does the weather have an effect on price?
* What car year has the best condition?
* Is price affected by manufacturer?
* Does car size affect sales price?
* Which state has the most expensive/least expensive cars, as well as the best condition of cars for sale?
