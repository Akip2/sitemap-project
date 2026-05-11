import time

from flask import Flask, render_template, jsonify, request
from BdMongo import get_articles, insert_source, get_sources, update_source, insert_articles, delete_source, delete_articles_from_source
from utils import treat_int_input, treat_str_input, trear_array_input
from sitemap_parser import get_source_name, parse
from collections import Counter
from apscheduler.schedulers.background import BackgroundScheduler

EXCLUDED_WORDS = ["dans", "au", "aux", "il", "elle", "ils", "elles", "nous", "vous", "tu", "je", "pas", "ne", "ma", "mon", "mes", "sur", "sous", "entre", "ses", "sa", "son", "se", "ce", "cette", "cet", "quel", "quelle", "quels", "quelles", "quand", "que", "qui", "quoi", "dont", "comment", "pourquoi" "on", "où", "là", "le", "la", "les", "un", "une", "de", "des", "du", "avec", "or", "pour", "et", "à", "avec", "par"]
EXCLUDED_CHARS = ["…", ".", ",", "!", "?", ":", ";", "%", "€", "$", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "«", "»", "n’", "l’", "qu’", "d’", "d'", "j’", "m’"]

def get_title_words(title):
    formatted_title = title.replace("\n", " ").replace("/", " ").lower()
    for c in EXCLUDED_CHARS:
        formatted_title = formatted_title.replace(c, "")

    word_array = formatted_title.split()
    word_array = [w for w in word_array if not w in EXCLUDED_WORDS]

    word_dict = {}
    for w in word_array:
        if w in word_dict.keys():
            word_dict[w] += 1
        else:
            word_dict[w] = 1

    return word_dict

def check_for_updates():
    sources = get_sources()
    currentTime = time.time()

    for source in sources:
        update_time = source["last_update"] + source["time_interval"]
        if(currentTime >= update_time):
            articles = parse(source["name"], source["url"])
            insert_articles(articles)
            update_source(source["name"], currentTime)

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
@app.route("/consultation")
@app.route("/list")
def article_list():
    return render_template("list.html", page="consultation", subpage="list")

@app.route("/cloud")
def cloud():
    return render_template("cloud.html", page="consultation", subpage="cloud")

@app.route("/admin")
def admin():
    return render_template("admin.html", page="admin")

#API ROUTES TO GET DATA
@app.route("/api/articles", methods=["GET"])
def api_articles():
    origin  = treat_str_input(request.args.get("origin"))
    keywords = trear_array_input(request.args.get("keywords"))
    date_start = treat_str_input(request.args.get("date_start"))
    date_end = treat_str_input(request.args.get("date_end"))

    articles = get_articles(origin, date_start, date_end, keywords)
    return jsonify(articles)

@app.route("/api/sources", methods=["POST", "GET"])
def api_sources():
    if(request.method == "POST"):
        json = request.get_json()
        url = json.get("url")
        time_interval = json.get("time_interval")

        try:
            name = get_source_name(url)

            articles = parse(name, url)
            insert_articles(articles)

            source = {
                "name": name,
                "url": url,
                "last_update": time.time(),
                "time_interval": time_interval
            }
            insert_source(source)
            
            return {"message": "Source ajoutée avec succès"}, 200
        except:
            return {"error": "Sitemap invalide"}, 400

    elif(request.method == "GET"):
        sources = get_sources()
        return jsonify(sources)

@app.route("/api/sources/<name>", methods=["DELETE"])
def api_sources_delete(name):
    delete_source(name)
    delete_articles_from_source(name)
    
    return {"message": "Source supprimée"}, 200

@app.route("/api/wordcloud")
def api_wordcloud():
    nb_word  = treat_int_input(request.args.get("nb_word"))    
    origin  = treat_str_input(request.args.get("origin"))
    date_start = treat_str_input(request.args.get("date_start"))
    date_end = treat_str_input(request.args.get("date_end"))

    articles = get_articles(origin, date_start, date_end, None)

    result_dic = Counter()
    for article in articles:
        result_dic += Counter(get_title_words(article["title"]))

    if(nb_word != None):
        result_dic = result_dic.most_common(nb_word)

    return jsonify(result_dic)

scheduler = BackgroundScheduler()
scheduler.add_job(check_for_updates, 'interval', minutes=1)

check_for_updates()
scheduler.start()
app.run(debug=True)