import os
from flask import Flask
from pandas.io.data import DataReader
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    goog = DataReader("GOOG",  "yahoo", datetime(2000,1,1), datetime(2012,1,1))
    return str(goog["Adj Close"].describe()["mean"])
