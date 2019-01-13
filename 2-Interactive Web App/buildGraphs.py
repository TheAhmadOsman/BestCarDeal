import pandas as pd
import numpy as np
import matplotlib
#multithreading to prevent crashes
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os.path
import folium
import operator
import time
from folium import plugins
from flask import make_response

def lineGraphAvg(data, form):
    x = form.fltOne.data
    y = form.fltTwo.data
    cat = form.cat.data
    fileName = "static/{}+{}+{}+line.png".format(x, y, cat)    
    exists = os.path.isfile(fileName)
    if exists:
        return fileName
    if x != "year" and y != "weather":
        data[x] = data[x].round(decimals=-3)
    if y != "year" and y != "weather":
        data[y] = data[y].round(decimals=-3)
    medianY = data.groupby(x)[y].median()
    medianYRolling = medianY.rolling(25).mean()
    xData = medianYRolling.index.values
    yData = medianYRolling.values
    fig, ax = plt.subplots(figsize = (16, 16))
    ax.set_ylabel(y)
    ax.set_xlabel(x)
    if cat != "no_category":
        ax.set_title("{} and {} by {}".format(x.title(), y.title(), cat.title()))        
        ax.plot(xData, yData, label="All {}s".format(cat))        
        catValues = data[cat].value_counts()
        for i in catValues.iteritems():
            catData = data[data[cat].values == i[0]]
            medianY = catData.groupby(x)[y].median()
            medianYRolling = medianY.rolling(25).mean()
            xData = medianYRolling.index.values
            yData = medianYRolling.values
            ax.plot(xData, yData, label=i[0])
        ax.legend(loc="upper left")
    else:
        ax.set_title("{} and {}".format(x.title(), y.title()))
        ax.plot(xData, yData)                
    plt.savefig(fileName)
    plt.clf()    
    return fileName

def pieCharts(data, form):
    cat = form.cat.data
    fileName = "static/{}+pie.png".format(cat)
    exists = os.path.isfile(fileName)
    if exists:
        return fileName
    catValues = data[cat].value_counts()
    catCounts = []
    catStrVals = []
    if cat == "year":
        base = 1900
        for i in range(12):
            i = i * 10
            catStrVals.append("{} - {}".format(str(base + i), str(base + i + 9)))
            catCounts.append(data[data["year"].between(base + i, base + i + 9, inclusive = True)]["year"].count())
    else:
        sumVals = data[cat].count()        
        for i in catValues.iteritems():
            catStrVals.append("{} - {:.3%}".format(i[0], i[1] / sumVals)) 
            catCounts.append(i[1])
    fig, ax = plt.subplots(figsize=(16, 16))
    colors = reversed(["indianred", "red", "orangered", "chocolate", "saddlebrown",
              "orange", "gold", "yellow", "yellowgreen", "greenyellow", "limegreen",
              "mediumseagreen", "mediumaquamarine", "turquoise", "deepskyblue", "dodgerblue",
              "royalblue", "darkblue", "mediumpurple", "darkviolet", "purple", "mediumvioletred",
              "crimson"])
    patches, texts = ax.pie(catCounts, startangle = 90, shadow = True, colors = colors)
    ax.axis("equal")
    plt.legend(patches, catStrVals, loc="best")
    plt.savefig(fileName)
    plt.clf()
    return fileName

def genericBarGraph(data, form):
    categorical = form.catDropdown.data
    floating = form.fltDropdown.data
    fileName = "static/{}+{}+bar.png".format(categorical, floating)
    exists = os.path.isfile(fileName)
    if exists:
        return fileName
    uniqueCategorical = data[categorical].value_counts()
    uniqueList = []
    floatingMedians = []
    sortingDict = {}
    for i in uniqueCategorical.iteritems():
        sortingDict[i[0]] = data[floating][data[categorical].values == i[0]].mean()
    sortedItems = sorted(sortingDict.items(), key=operator.itemgetter(1))
    for i in reversed(sortedItems):
        uniqueList.append(i[0])
        floatingMedians.append(i[1])
    plt.bar(uniqueList, floatingMedians)
    if categorical == "manufacturer" or categorical == "type" or categorical == "state_name":
        plt.xticks(rotation=90)
    if floating == "year":
        axes = plt.gca()
        axes.set_ylim([1960,2020])        
    plt.xlabel(categorical)
    plt.ylabel(floating)
    plt.gcf().subplots_adjust(bottom=0.3)
    fig = plt.gcf()
    fig.set_size_inches(10, 8)
    plt.savefig(fileName)
    plt.clf()
    return fileName
    
def buildHeatmap(data, cat, var):
    if cat != "year" and cat != "odometer" and cat != "price" and cat != "weather":
        uniqueData = data.loc[data[cat] == var]
    else:
        var = var.split("-")
        varLow = int(var[0])
        varHigh = int(var[1])
        uniqueData = data[(data[cat] >= varLow) & (data[cat] <= varHigh)]
    uniqueData = uniqueData[(uniqueData["state_name"] != "FAILED")]
    uniqueData = uniqueData[np.isfinite(uniqueData["lat"])]
    carMap = folium.Map(location = [41, -96], zoom_start=4)
    heatArr = uniqueData[["lat", "long"]].as_matrix()
    carMap.add_child(plugins.HeatMap(heatArr, radius=15))
    html = carMap.get_root().render()
    return html


def buildQuantileFrame(data, x, y, cat):
    
    xQuantiles = [0]
    quantileData = {}
    percentileHTML = []
    allData = False
    if cat != "No Category":
        catVals = data[cat].value_counts()
        varList = []
        for i in catVals.iteritems():
            varList.append(i[0])
    else:
        varList = ["All Categories"]
        allData = True
        
    for var in varList:
        
        if allData == False:
            catData = data[data[cat].values == var]
        else:
            catData = data
        
        for i in range(10):
            xQuantiles.append(catData[x].quantile((i+1)/10))
            
        for i in range(10):
            xQuantilesFrame = catData[catData[x].between(xQuantiles[i], xQuantiles[i+1])]
            yQuantiles = [0]
            yMeans = []
            for j in range(10):
                yQuantiles.append(xQuantilesFrame[y].quantile((j+1)/10))
            for j in range(10):
                yQuantilesFrame = xQuantilesFrame[xQuantilesFrame[y].between(yQuantiles[j], yQuantiles[j+1])]
                yMean = yQuantilesFrame[y].mean()
                try:
                    yMeans.append(int(yMean))
                except:
                    yMeans.append("No Info")
            quantileData["{}-{}".format(round(xQuantiles[i]), round(xQuantiles[i+1]))] = yMeans
        percentileHTML.append([var, pd.DataFrame(quantileData).to_html()])
        
    return percentileHTML

