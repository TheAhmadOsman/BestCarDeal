from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired
import buildGraphs
import retrieveData

app = Flask(__name__)
# so very secret...
app.config['SECRET_KEY'] = "CraigsistCars+TrucksVisualization"
bootstrap = Bootstrap(app)

DATASET_NAME = "cars.csv"

DATA = retrieveData.createDataset(DATASET_NAME)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", msg = None)

@app.route("/barGraphs", methods=["GET", "POST"])
def barGraphs():
    try:
        form = retrieveData.getBarGraphCriteria()
        if form.is_submitted():
            img = buildGraphs.genericBarGraph(DATA, form)
            return render_template("barGraphs.html", form = form, img = img)
        return render_template("barGraphs.html", form = form, img = None)
    except Exception as e:
        return render_template("index.html", msg = f"Something went wrong, please try again: {e}")        

@app.route("/lineGraphs", methods=["GET", "POST"])
def lineGraphs():
    try:
        form = retrieveData.getLineGraphCriteria()
        if form.is_submitted():
            img = buildGraphs.lineGraphAvg(DATA, form)
            return render_template("lineGraphs.html", form = form, img = img)
        return render_template("lineGraphs.html", form = form, img = None)
    except Exception as e:
        return render_template("index.html", msg = f"Something went wrong, please try again: {e}")        

@app.route("/pieCharts", methods=["GET", "POST"])
def pieCharts():
    try:
        form = retrieveData.getPieChartCriteria()
        if form.is_submitted():
            img = buildGraphs.pieCharts(DATA, form)
            return render_template("pieCharts.html", form = form, img = img)
        return render_template("pieCharts.html", form = form, img = None)
    except Exception as e:
        return render_template("index.html", msg = f"Something went wrong, please try again: {e}")        

@app.route("/heatMaps", methods=["GET", "POST"])
def heatMap():
    try:
        form = retrieveData.getHeatMapCriteria()
        cat = form.cat.data
        firstDrop = False
        if form.is_submitted():
            form = retrieveData.getHeatMapCriteria(cat, DATA)            
            firstDrop = True
            return render_template("heatMaps.html", form = form, firstDrop = firstDrop)
        return render_template("heatMaps.html", form = form, firstDrop = firstDrop)
    except Exception as e:
        return render_template("index.html", msg = f"Something went wrong, please try again: {e}")
    

@app.route("/renderMap", methods=["GET", "POST"])
def renderMap():
    try:
        form = retrieveData.getHeatMapCriteria()
        cat = form.cat.data
        var = form.var.data
        html = buildGraphs.buildHeatmap(DATA, cat, var)
    except Exception as e:
        return render_template("index.html", msg = f"Something went wrong, please try again: {e}")
    return html

@app.route("/countMap", methods=["GET"])
def countMap():
    return redirect("https://plot.ly/~reesau01/2/")

@app.route("/priceMap", methods=["GET"])
def priceMap():
    return redirect("https://plot.ly/~reesau01/4/")

@app.route("/quantiles", methods=["GET", "POST"])
def quantiles():
    #try:
        form = retrieveData.getQuantilesCriteria()
        if form.is_submitted():
            x = form.x.data
            y = form.y.data
            cat = form.cat.data
            htmlList = buildGraphs.buildQuantileFrame(DATA, x, y, cat)
            return render_template("quantiles.html", form = form, htmlList = htmlList, x = x, y = y)        
        return render_template("quantiles.html", form = form, text = None)
    #except Exception as e:
        #return render_template("index.html", msg = f"Something went wrong, please try again: {e}")
        

if __name__ == "__main__":
    app.run(debug=True)
