from flask import Flask, jsonify, request, render_template

app = Flask("server")

@app.route("/", methods=["GET"])
def index():
    return render_template("frontend.html")

@app.route("/scrape", methods=["GET"])
def scraper():
    try:
        req = request.get_json()
        url = req.get("url")
        
        