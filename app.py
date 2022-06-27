from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import json, random
from gpapi.getproxies import GimmeProxyApi

app = Flask(__name__)
ssl._create_default_https_context = ssl._create_unverified_context

URL = "https://kalimatimarket.gov.np/"
# URL = "https://nepalicalendar.rat32.com/vegetable/"

SECRET = "lWqBcOoELieSOtVzoeJb_*Sv0$yx6QQzG7z@v)ieY=wlm(_!E3YQvFXL=6"

HEADER = {
    'User-Agent': 'Mozilla/6.5 AppleWebKit/537.50 (KHTML, like Gecko) Chrome/101.0.4951.45',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
    'refere': 'https://www.google.com/search?q=aaja+ko+tarkari&oq=aaja+ko+tarkari&aqs=chrome..69i57.11059j0j1&sourceid=chrome&ie=UTF-8',
}
user_agent_list = (
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
)


@app.route("/")
def home():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    try:
        api = GimmeProxyApi() 
        random_proxy = api.get_proxy()
        # page = requests.get(URL, headers=HEADER)
        page = requests.get(URL, headers={"User-Agent":random.choice(user_agent_list)}, proxies=random_proxy)
        soup = BeautifulSoup(page.content, "html.parser")
        print(soup)
        priceTable = soup.find(id="commodityPricesDailyTable")
        date = priceTable.find_all("h5")[0].text
        # date = priceTable.find(id="vtitle").text
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


    # api = GimmeProxyApi() 
    # random_proxy = api.get_proxy()
    # page = requests.get(URL, headers={"User-Agent":random.choice(user_agent_list)}, proxies=random_proxy)
    # soup = BeautifulSoup(page.content, "html.parser")
    # priceTable = soup.find(id="commodityPricesDailyTable")
    # # date = priceTable.find_all("h5")[0].text
    # date = priceTable.find(id="vtitle").text
    # table = soup.find(id="commodityDailyPrice")
    # data = []
    # for tr in table.find_all("tr"):
    #     data_td = []
    #     for td in tr.findAll("td"):
    #         data_td.append(td.text.strip())
    #     if len(data_td) > 0:
    #         data.append(data_td)
    # return jsonify({"date": date, "data": data})


@app.route("/pd")
def tables():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    tables = pd.read_html(URL)
    df = tables[0]
    data = json.dumps(json.loads(df.to_json(orient="records")))
    return data
