from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

URL = "https://kalimatimarket.gov.np/"

@app.route("/")
def home():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="commodityDailyPrice")

    data = []
    for tr in results.find_all("tr"):
        data_td = []
        for td in tr.findAll("td"):
            if len(data) == 0:
                data.insert(0, td.text.strip())
            else:
                data_td.append(td.text.strip())
        print()
        data.append(data_td)
    return jsonify(data)

@app.route("/pd")
def pd():
    tables=pd.read_html(URL)
    # tables[0]
    return "tables[0].to_json()"
    