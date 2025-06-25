import os
from flask import Flask, render_template, redirect, request
from supabase import create_client, Client
import scraper
import time

app = Flask(__name__)
# flask run --debug


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/load", methods=["POST"])
def load():
    data = request.get_json()
    driver = scraper.open_driver()
    fit = scraper.check_fit(data["url"], driver)
    driver.close()
    return {"fit": fit}