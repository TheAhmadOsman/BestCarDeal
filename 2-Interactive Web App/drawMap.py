from retrieveData import createDataset
import plotly as py
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

FILE_NAME = "craigslistVehiclesFull.csv"

KEY = open("secretKey.txt", "r").readline().strip()

py.tools.set_credentials_file(username="reesau01", api_key=KEY)

def drawCountsMap(data):
    
    counties = data.groupby(by='county_fips', as_index=False).agg({'url': pd.Series.nunique})
    counties = counties.rename(columns={"url": "fip_count"})
    
    fips = counties.county_fips.astype("int").tolist()
    counts = counties.fip_count.tolist()
    
    fig = ff.create_choropleth(
        fips = fips,
        values = counts,
        county_outline = {'color': 'rgb(255,255,255)', 'width': 0.5}, 
        title='Cars for sale across America',
        showlegend = False
    )
    
    py.plotly.plot(fig, filename="carSales")
        
    
def drawMeanMap(data):
    countyMeans = data.groupby(by = "county_fips", as_index = False)["price"].mean()
    
    fips = countyMeans.county_fips.astype("int").tolist()

    avgPrices = countyMeans.price.fillna(0).astype("int").tolist()
    
    reducedPrices = []
    for i in avgPrices:
        reducedPrices.append(i // 10)
    
    fig = ff.create_choropleth(
        fips = fips,
        values = reducedPrices,
        county_outline = {'color': 'rgb(255,255,255)', 'width': 0.5}, 
        title='Average Price by County',
        showlegend = False
    )
    
    py.plotly.plot(fig, filename="avgPrices")        
    
    
def main():
    data = createDataset(FILE_NAME)
    drawCountsMap(data)
    drawMeanMap(data)
    
if __name__ == "__main__":
    main()