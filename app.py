#web app

from flask import Flask, render_template, request
import joblib
import os

# Load the model from the same folder as app.py (works no matter where you run it from)
model = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dbs.pkl"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    q = request.form.get("q")
    return render_template("main.html", name=q)

@app.route("/dbs", methods=["GET", "POST"])
def dbs():
    return render_template("dbs.html")

@app.route("/dbsResult", methods=["GET", "POST"])
def dbsResult():
    q = request.form.get("q")
    if not q:                                   # empty box -> go back to the input page
        return render_template("dbs.html", error="Please enter an exchange rate.")
    q = float(q)
    r = model.predict([[q]])
    r = float(r.ravel()[0])                     # flatten [[35.42]] -> 35.42
    return render_template("dbsResult.html", q=q, r=round(r, 2))

if __name__ == "__main__":
    app.run(debug=True)