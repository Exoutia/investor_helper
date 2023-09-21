from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
import json
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mutualFund.db"
db = SQLAlchemy(app)

api_url = "https://api.mfapi.in/mf/"

# assets
assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()


class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheme_code = db.Column(db.Integer, nullable=False)
    scheme_name = db.Column(db.String(100), nullable=False)

    def __repl__(self):
        return f"<scheme_code: {self.scheme_code} scheme_name: {self.scheme_name}>"


@app.route("/")
def index():
    spinner = "static/svg/svg-loaders/spinning-circles.svg"
    return render_template("index.html", spinner=spinner)


@app.route("/search-bar")
def search_bar():
    spinner = "static/svg/svg-loaders/spinning-circles.svg"
    return render_template("search-bar.html", spinner=spinner)


@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        mutual_funds = (
            MutualFund.query.filter(
                MutualFund.scheme_name.icontains(query)
                | MutualFund.scheme_code.icontains(query)
            )
            .limit(100)
            .all()
        )
        if not mutual_funds:
            mutual_funds = ""
    else:
        mutual_funds = MutualFund.query.limit(100).all()

    spinner = "static/svg/svg-loaders/spinning-circles.svg"
    return render_template("search-results.html", results=mutual_funds, spinner=spinner)


@app.route("/mutualfunds/<scheme_code>")
def funds_detials(scheme_code):
    response = requests.get(api_url + scheme_code + "/latest")
    if response.status_code == 200:
        mutual_fund_result = response.json()
    else:
        mutual_fund_result = None

    spinner = "static/svg/svg-loaders/spinning-circles.svg"
    # print("hi:", mutual_fund_result)
    return render_template(
        "mutualfundsDetails.html", result=mutual_fund_result, spinner=spinner
    )


def load_data():
    data = json.loads(open("mutualfunds.json").read())
    for row in data:
        mf = MutualFund(scheme_code=row["schemeCode"], scheme_name=row["schemeName"])
        db.session.add(mf)
    db.session.commit()
    print("Done")


if __name__ == "__main__":
    app.run(debug=True)
