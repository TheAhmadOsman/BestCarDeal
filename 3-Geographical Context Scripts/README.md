# Geographical Context Scripts

## Context

As we began, we assumed that our data having longitudes and latitudes would make this quest an easy one, but such is life. First, we have to understand that our data at this point is very big, and that a simple API would not let us make 1.7 million calls, and then we have to also know that sqlite does not support concurrent tasks and would only allow one entry to be updated per database.

We tried searching for any database that would provide us the State and the Country given that we pass in longitude and latitude, but all our efforts were not successful. At one point, we almost gave up on this task, especially that the kind of providers we could find were either unreliable or quite expensive.

Fortunately, we came across a Federal website that among the data they'd provide you given a longitude and a latitude were what we have been looking for. The [Federal Communications Commission Area API](https://geo.fcc.gov/api/census/#!/area/get_area) allowed us to send in a longitude and latitude, and to get the following data:

* county_name
* county_fips
* state_code
* state_name
* state_fips

If you think about it, this is an awesome tool provided by the American Government, and the fact that we were able to not only collect the relative data of 1,700,000 entries but also to do that in under 2 hours is even more impressive. Long story short, we implemented a multi-threaded program that made about 15,000 requests per minute. We also had to migrate from Sqlite to PostgreSQL, since the former did not have any multi-threading support.

All in all, we were able to to get the geographical data we wanted for 1,700,000 entries, and not only to that for this huge amount of data, but to also do it within two hours, which seemed impossible when we started. We had some failed responses but that is because the sent longitudes and latitudes belonged to Canada, and this failed responses helped us get rid of any entries outside of the United States.

## Usage

You will need to get the scraped data exported into CSV and then imported into a PostgreSQL. Then you will need to change the db connection configurations in threadomg-psql.py and then simply run `python3 threadomg-psql.py`.
