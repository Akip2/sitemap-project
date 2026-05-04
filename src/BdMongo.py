from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client.get_database("SD2026_projet")

def generate_prefixed_collection_name(name):
    return "G_FFST_"+name

def get_collection(name):
    return database.get_collection(generate_prefixed_collection_name(name))

def insert_articles(articles):
    article_collection = get_collection("articles")
    for article in articles:
        article_collection.update_one(
            {"loc": article["loc"]},
            {"$set": article},
            upsert=True
        )

def get_articles(origin, date_start, date_end, keywords):
    collection = get_collection("articles")

    filter = {}

    if(origin != None):
        filter["origin"] = origin

    if(keywords != None):
        filter["title"] = {"$regex": "|".join(keywords), "$options": "i"}

    if(date_start != None) or (date_end != None):
        filter["publication_date"] = {}
        if date_start != None:
            filter["publication_date"]["$gte"] = date_start
        if date_end != None:
            filter["publication_date"]["$lte"] = date_end

    return list(collection.find(filter, {"_id": 0}))