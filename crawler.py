import requests
import json
from collections import defaultdict
from app.models import Hotel
from app import db

headers = {"accept-language": "en-GB","user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78:.0.3904.70 Safari/537.36","content-type": "application/json","accept": "*/*"} 

hotel_data = []

def run(start_date,final_date,page):
    if page==125:
        db.session.add_all(hotel_data)
        db.session.commit()
        return hotel_data
    query = {
        "tz":-60,
        "pra":"",
        "channel":"b,isd:0",
        "csid":5,
        "ccid":"Xdkd2nONn2kEZ28UZnqK-AAAADQ",
        "adl":3,
        "crcl":"39.814838/21.427378,20000",
        "s":"0",
        "uiv":"67009/200:1",
        "tid":"YY9BMA212mjCZhOSJk1PC4Edm_",
        "sp":f"{start_date}/{final_date}",
        "rms":"2",
        "p":"uk",
        "l":"en-GB",
        "ccy":"SAR",
        "accoff":page,
        "acclim":25
    }
    data = {"operationName":"regionSearchKotlin","variables":{"searchType":"cep.json","queryParams":json.dumps(query),"pollData":None,"isAirBnbSupported":True,"openItemsInNewTab":False,"areUSPsSupported":False,"showHomeAwayPremierProperties":False,"showGranularAAccType":False,"isMobileList":False,"skipAlternativeDeals":False,"skipMinPriceExtraInfo":True,"shouldSkipRedirect":False},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"ad442c8750ff005fe2161afe3f2c4a783f6d5d432c9ef3039b7d2db8019ddd83"}}}

    html = requests.post("https://cdn-hs-graphql-dus.trivago.com/graphql",headers=headers,data=json.dumps(data))
    
    if html.status_code==200:
        data_js = html.json()
        hotels = data_js.get('data',
            {'rs2':
                {'accommodations':{}}
            }
        ).get('rs2').get('accommodations')
    else:
        return run(start_date,final_date,page)

    if not hotels:
        print(f'page : {page} not fetched...')
        return run(start_date,final_date,page)
    
    else:
        print(f'page : {page} fetched...')
        for hotel in hotels:
            name = hotel['name']['value']
            price = 'SAR ' + str(hotel['deals']['bestPrice']['pricePerStay'])
            alternatives = {'data':[]}
            for alt in hotel['deals']['alternative']:
                alternatives['data'].append({
                        'name':alt['name']['value'],
                        'price':'SAR ' + str(alt['price'])+'/night'
                    }
                )
            hotel_data.append(Hotel(name=name,price=price,start_date=start_date,final_date=final_date,alternative=alternatives))
    return run(start_date,final_date,page+25)

    