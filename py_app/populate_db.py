import calendar
import requests
import pymongo
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='./populate_db.log', filemode='a')

url = "http://numbersapi.com/"
headers = {'Content-Type': 'text/plain; charset=utf-8'}
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["facts_db"]
col = db["facts"]

cal = calendar.Calendar()
id = 1
db_input_list = list()
for month in range(1, 13):
    for day in cal.itermonthdates(2020, month):
        if day.year == 2020 and day.month == month:
            try:
                response = requests.get("{}{}/date".format(url, day.strftime('%m/%d')), headers=headers)
                logging.debug("Response from numbersapi.com: {}".format(response.content.decode("utf8")))
            except requests.exceptions.RequestException as err:
                logging.error("An error encountered while sending a HTTP request: \"{}\".".format(err))
                response = None
            if response:
                input_data = {"id": id, "month": day.strftime('%B'), "day": int(day.strftime('%d')), "fact": response.content.decode("utf8"), "hits": 0}
                logging.debug("input data: {}".format(input_data))
                db_input_list.append(input_data)
                #result = col.insert_one(input_data)
            id += 1
col.insert_many(db_input_list)
