from flask import Flask, render_template, jsonify
from BdMongo import get_articles

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
@app.route("/api/articles")
def api_articles():
    articles = get_articles()
    return jsonify(articles)

app.run(debug=True)