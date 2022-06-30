from flask import current_app as app, jsonify
import random, requests
from gpapi.getproxies import GimmeProxyApi
from datetime import datetime
from .models import MyData, db, Price
from bs4 import BeautifulSoup
from application.constants import URL, user_agent_list
from . import scheduler

# check if provided date is today
def isToday(date):
    now = datetime.today().date()
    print("Now: {}, Date: {}".format(now, date.date()))
    try:
        return date.date() == now
    except:
        return False

# gegt the price list from the api
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

# get the formatted prices as a list  
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

# save data to db 
def saveToDB():
    prices = getPricesFromAPI()
    date = prices['date']
    data = prices['data']
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

# calls [saveToDB] and return http response
def saveAndRespond():
    print("Getting from API")
    result = saveToDB()
    return jsonify({ "date": result['date'], "data": result['data']})

#  Cronjob method to save the data to DB 
def saveToDBCronJob():
    print("================ Cronjob started: {} ================".format(datetime.today().strftime("%d %b, %Y | %-I:%-M %p")))
    hour = datetime.today().strftime("%-H")
    if hour <=5 or hour >=13:
        print("================ Cronjob cancelled | Time: {} ================".format(hour))
    else:
        prices = getPricesFromAPI()
        date = prices['date']
        data = prices['data']
        print("Saving to DB for: {}".format(date))
        with scheduler.app.app_context():
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
        print("================ Cronjob ended ================")