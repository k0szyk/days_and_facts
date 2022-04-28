import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["facts_db"]
col = db["facts"]

for item in col.find():
    print(item)
