
from flask import current_app as app, jsonify, request

from application.constants import URL, SECRET
from .models import MyData
import pandas as pd
from . import utility
import json

@app.route("/", methods=['GET'])
def home():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    forceUpdate = request.args.get('forceUpdate')
    if(forceUpdate != None):
        return utility.saveAndRespond()
    else:
        existing_data = MyData.query.get(1)
        try:
            if(existing_data):
                print("Existing Data: {}".format(existing_data.date))
                return jsonify({"date": existing_data.date, "data": utility.getPricesList(existing_data.prices)})
            else: 
                print("New Data")
                return utility.saveAndRespond()
        except:
            print("Error")
            return jsonify({"error": "Error"})

@app.route("/pd")
def tables():
    dt = request.args.get('dt')
    if(dt != SECRET):
        return jsonify({"error": "A BIG NO NO"})
    tables = pd.read_html(URL)
    df = tables[0]
    data = json.dumps(json.loads(df.to_json(orient="records")))
    return data
