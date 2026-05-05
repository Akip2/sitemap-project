from flask import Flask, render_template, jsonify, request
from BdMongo import get_articles, insert_source, get_sources
from utils import treat_str_input, trear_array_input
from sitemap_parser import get_source_name

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

        try:
            name = get_source_name(url)

            source = {
                "name": name,
                "url": url
            }
            insert_source(source)
            
            return {"message": "Source ajoutée avec succès"}, 200
        except:
            return {"error": "Sitemap invalide"}, 400

    elif(request.method == "GET"):
        sources = get_sources()
        return jsonify(sources)
    

app.run(debug=True)