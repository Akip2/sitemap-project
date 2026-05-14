from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
database = client.get_database("SD2026_projet")

def set_up_indexes():
    article_collection = get_collection("articles")

    article_collection.create_index({"origin": 1})
    article_collection.create_index({"publication_date": 1})
    article_collection.create_index({"last_consultation": 1})

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

def insert_source(source):
    sources_collection = get_collection("sources")
    sources_collection.update_one(
        {"name": source["name"]},
        {"$set": source},
        upsert=True
    )

def get_sources():
    sources_collection = get_collection("sources")

    return list(sources_collection.find({}, {"_id": 0}))

def delete_source(name):
    sources_collection = get_collection("sources")
    sources_collection.delete_one({"name": name})

def update_source(name, update_time):
    sources_collection = get_collection("sources")
    sources_collection.update_one({"name": name}, {"$set": {"last_update": update_time}})

def delete_articles_from_source(source_name):
    article_collection = get_collection("articles")
    article_collection.delete_many({"origin": source_name})    

def update_consultation(loc, timestamp):
    article_collection = get_collection("articles")
    article_collection.update_one(
        {"loc": loc},
        {"$set": {"last_consultation": timestamp}}
    )

def get_articles(origin, date_start, date_end, keywords, consultation_date=None, consultation_time=None):
    article_collection = get_collection("articles")

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

    if consultation_date or consultation_time:
        conditions = []
        if consultation_date:
            start_dt = datetime.strptime(consultation_date, '%Y-%m-%d')
            start_ts = start_dt.timestamp()
            end_ts = start_ts + 86400
            conditions.append({"last_consultation": {"$gte": start_ts, "$lt": end_ts}})
        if consultation_time:
            h, m = map(int, consultation_time.split(':'))
            offset = h * 3600 + m * 60
            conditions.append({"$expr": {"$eq": [{"$mod": ["$last_consultation", 86400]}, offset]}})
        if len(conditions) == 1:
            filter.update(conditions[0])
        else:
            filter["$and"] = conditions

    return list(article_collection.find(filter, {"_id": 0}).sort("publication_date", -1))

set_up_indexes()