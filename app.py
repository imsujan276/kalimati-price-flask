from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import json

app = Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context

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
                data_td.append(td.text.strip())
        if len(data_td) > 0:
            data.append(data_td)
    return jsonify(data)

@app.route("/pd")
def tables():
    tables=pd.read_html(URL)
    df = tables[0]
    data = json.dumps(json.loads(df.to_json(orient="records")))
    return data
    