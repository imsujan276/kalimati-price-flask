from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import json
from urllib.request import Request, urlopen

app = Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context

URL = "https://kalimatimarket.gov.np/"
SECRET = "lWqBcOoELieSOtVzoeJb_*Sv0$yx6QQzG7z@v)ieY=wlm(_!E3YQvFXL=6"
HEADER = {
  'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
  'Accept-Encoding': 'none',
  'Accept-Language': 'en-US,en;q=0.8',
  'Connection': 'keep-alive',
  'refere': 'https://duckduckgo.com',
  'cookie': """"""
}

@app.route("/")
def home():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    try:
        page = requests.get(URL, headers=HEADER)
        # page = requests.get(URL, headers={'User-Agent': 'Mozilla/6.0'})
        soup = BeautifulSoup(page.content, "html.parser")

        priceTable = soup.find(id="commodityPricesDailyTable")
        date = priceTable.find_all("h5")[0].text

        table =  soup.find(id="commodityDailyPrice")
        data = []
        for tr in table.find_all("tr"):
            data_td = []
            for td in tr.findAll("td"):
                    data_td.append(td.text.strip())
            if len(data_td) > 0:
                data.append(data_td)
        return jsonify({"date": date,"data": data})
    except:
        return jsonify({"error": "ERROR"})

@app.route("/pd")
def tables():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    tables=pd.read_html(URL)
    df = tables[0]
    data = json.dumps(json.loads(df.to_json(orient="records")))
    return data
    