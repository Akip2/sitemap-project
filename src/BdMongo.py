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

def get_articles():
    collection = get_collection("articles")

    filter = {}

    return collection.find(filter)