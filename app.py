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
    data["min_followers"] = 0 if data["min_followers"] == "" else int(data["min_followers"])
    data["min_employees"] = 0 if data["min_employees"] == "" else int(data["min_employees"])
    data["max_followers"] = 0 if data["max_followers"] == "" else int(data["max_followers"])
    data["max_employees"] = 0 if data["max_employees"] == "" else int(data["max_employees"])

    driver = scraper.open_driver()
    companies = data["companies"]
    results = {}
    for c in companies:
        url = c.lower()
        url = url.replace(" ", "-")
        url = f"https://www.linkedin.com/company/{url}/"
        fit = scraper.check_fit(url, driver, data)
        results[c] = fit
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.close()
    return results