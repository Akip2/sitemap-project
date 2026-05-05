import time

from flask import Flask, render_template, jsonify, request
from BdMongo import get_articles, insert_source, get_sources, insert_articles, delete_source, delete_articles_from_source
from utils import treat_str_input, trear_array_input
from sitemap_parser import get_source_name, parse

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

app.run(debug=True)