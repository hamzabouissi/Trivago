from flask import Flask,request
from flask.json import jsonify
#from models import Hotel
from app import app,db
from app.models import Hotel
from crawler import run






@app.route('/crawler',methods=['GET',])
def hello_world():
    hotels_data = []
    start_date = request.args.get('start_date','').replace('-',"")
    final_date = request.args.get('final_date','').replace('-',"")
    

    db_data = run(start_date,final_date,0)
    for hotel in db_data:
        hotels_data.append(
            hotel.to_json()
        )
    return jsonify(hotels_data)

@app.route('/test')
def test():
    return {"test":"asdhajsda"}