from os import uname
from flask import current_app as app, jsonify, request
import flask

from application.constants import URL, user_agent_list, SECRET, HEADER
from .models import MyData, db, Price

from bs4 import BeautifulSoup
import pandas as pd
import json, random, requests
from gpapi.getproxies import GimmeProxyApi
from datetime import datetime

def isToday(date):
    now = datetime.today().date()
    hour = datetime.today().strftime('%H')
    print("Now: {}, hour: {}, Date: {}".format(now, hour, date.date()))
    try:
        return date.date() == now
    except:
        return False

def getPricesFromAPI():
    api = GimmeProxyApi() 
    random_proxy = api.get_proxy()
    page = requests.get(URL, headers={"User-Agent":random.choice(user_agent_list)}, proxies=random_proxy)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    priceTable = soup.find(id="commodityPricesDailyTable")
    date = priceTable.find_all("h5")[0].text
    table = soup.find(id="commodityDailyPrice")
    data = []
    for tr in table.find_all("tr"):
        data_td = []
        for td in tr.findAll("td"):
            data_td.append(td.text.strip())
        if len(data_td) > 0:
            data.append(data_td)
    return {"date": date, "data": data}

def getPricesList(prices):
    priceList = []
    for p in prices:
        pList = []
        pList.append(p.title)
        pList.append(p.unit)
        pList.append(p.min)
        pList.append(p.max)
        pList.append(p.avg)
        priceList.append(pList)
    return priceList

def saveToDB(date, data):
    print("Saving to DB for: {}".format(date))
    # clear all data
    Price.query.delete()
    MyData.query.delete()
    #add new data
    prices = []
    for d in data:
        p = Price(title=d[0],unit=d[1],min=d[2],max=d[3],avg=d[4])
        db.session.add(p)
        prices.append(p)

    myData = MyData(date=date, prices= prices)
    db.session.add(myData)
    db.session.commit()
    return {"date": date, "data": data}

def saveAndRespond():
    print("Getting from API")
    prices = getPricesFromAPI()
    result = saveToDB(prices['date'], prices['data'])
    return jsonify({ "date": result['date'], "data": result['data']})

@app.route("/", methods=['GET'])
def home():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    existing_data = MyData.query.get(1)
    try:
        if(existing_data):
            print("Existing Data: {}".format(existing_data.date))
            if(isToday(existing_data.created_date)):
                print("Today")
                return jsonify({"date": existing_data.date, "data": getPricesList(existing_data.prices)})
            else: 
                print("Not Today")
                return saveAndRespond()
                # prices = getPricesFromAPI()
                # if(prices['date'] == existing_data.date):
                #     return saveAndRespond()
                # else:
                #     return saveAndRespond()
        else: 
            print("New Data")
            return saveAndRespond()
    except:
        print("Error")
        return jsonify({"error": "Error"})


    # api = GimmeProxyApi() 
    # random_proxy = api.get_proxy()
    # page = requests.get(URL, headers={"User-Agent":random.choice(user_agent_list)}, proxies=random_proxy)
    # soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    # priceTable = soup.find(id="commodityPricesDailyTable")
    # date = priceTable.find_all("h5")[0].text
    # # date = priceTable.find(id="vtitle").text
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
