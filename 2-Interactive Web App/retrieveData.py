import pandas as pd
import numpy as np
import buildGraphs
from random import sample
from flask_wtf import FlaskForm
from wtforms import Form, SelectField, validators, StringField
from wtforms.validators import Length, ValidationError, DataRequired

categorical = [
    "manufacturer", "condition", "cylinders", "fuel", "year",
    "title_status", "transmission", "drive", "size", "type", "paint_color",
    "state_name"
]   

floaters = [
    "price", "year", "odometer", "weather"
]


def createDataset(fileName):
    
    skip = sorted(sample(range(2000000), 50000))
    data = pd.read_csv(fileName, skiprows = skip)
    return cleanData(data)
    
def cleanData(data):
    data.price = data.price[~((data.price-data.price.mean()).abs() > .05*data.price.std())]
    data.odometer = data.odometer[~((data.odometer-data.odometer.mean()).abs() > 3*data.odometer.std())]
    data.year = data.year[~((data.year-data.year.mean()).abs() > 10*data.year.std())]
    data.state_name = data.state_name.replace({"FAILED": "Outside United States"})
    return data

class getBarGraphCriteria(FlaskForm):
    ctg = []
    flt = []
    
    for i in categorical:
        ctg.append((i, i.title()))
    for i in floaters:
        flt.append((i, i.title()))
    
    catDropdown = SelectField("Category", choices = ctg)
    fltDropdown = SelectField("Numeric Value", choices = flt)

class getLineGraphCriteria(FlaskForm):
    ctg = [("no_category", "No Category")]
    flt = []
    
    for i in categorical:
        ctg.append((i, i.title()))
    for i in floaters:
        if i != "weather":
            flt.append((i, i.title()))
    cat = SelectField("Category", choices = ctg)
    fltOne = SelectField("X Axis", choices = flt)
    fltTwo = SelectField("Y Axis", choices = flt)
    
class getPieChartCriteria(FlaskForm):
    ctg = []
    for i in categorical:
        ctg.append((i, i.title()))
    
    cat = SelectField("Category", choices = ctg)

def getHeatMapCriteria(selectedCat = None, data = None):
    class HeatMap(FlaskForm):
        pass
    
    valList = []
    if selectedCat == None:
        ctg = []        
        for i in categorical:
            ctg.append((i, i.title()))
        for i in floaters:
            if i not in ctg:
                ctg.append((i, i.title()))
                
        cat = SelectField("Category", choices = ctg)
        
        var = SelectField("Variable", choices = valList)
    else:
        cat = SelectField("Category", choices = [(selectedCat, selectedCat.title())])        
        if selectedCat != "year" and selectedCat != "odometer" and selectedCat != "price" and selectedCat != "weather":
            vals = data[selectedCat].value_counts()
            for i in vals.iteritems():
                if i[0]:
                    valList.append((i[0], i[0].title()))
            var = SelectField("Variable", choices = valList)
        else:
            var = StringField("Between values (enter as follows: x-y)")
    setattr(HeatMap, "cat", cat)
    setattr(HeatMap, "var", var)
    return HeatMap()

class getQuantilesCriteria(FlaskForm):
    nums = []
    for i in floaters:
        nums.append((i, i.title()))
    cats = [("No Category", "No Category")]
    for i in categorical:
        if i != "year":
            cats.append((i, i.title()))
    x = SelectField("Group By Percentile", choices = nums)
    y = SelectField("Means Of", choices = nums)
    cat = SelectField("Category", choices = cats)
        
        
