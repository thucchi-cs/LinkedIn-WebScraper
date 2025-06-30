from flask import Flask, render_template, request, jsonify, redirect
import scraper
import tempfile
import shutil

app = Flask(__name__)
# flask run --debug

@app.route("/", methods=["POST", "GET"])
def index():
    return redirect("https://linkedin-webscraper.onrender.com/")
    # return render_template("index.html")

@app.route("/load", methods=["POST"])
def load():
    # try:
        data = request.get_json()
        data["min_followers"] = 0 if data["min_followers"] == "" else int(data["min_followers"])
        data["min_employees"] = 0 if data["min_employees"] == "" else int(data["min_employees"])
        data["max_followers"] = 0 if data["max_followers"] == "" else int(data["max_followers"])
        data["max_employees"] = 0 if data["max_employees"] == "" else int(data["max_employees"])
        
        for i in range(len(data["keywords"])):
            data["keywords"][i] = data['keywords'][i].lower()
        
        # print(data)
        user_data_dir = tempfile.mkdtemp()
        driver = scraper.open_driver(user_data_dir)
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
        driver.quit()
        shutil.rmtree(user_data_dir)
        return results
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500