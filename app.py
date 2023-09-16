from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mutualFund.db"
db = SQLAlchemy(app)


class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheme_code = db.Column(db.Integer, nullable=False)
    scheme_name = db.Column(db.String(100), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


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
    else:
        mutual_funds = MutualFund.query.limit(100).all()
    return render_template("search.html", results=mutual_funds)


def load_data():
    data = json.loads(open("mutualfunds.json").read())
    for row in data:
        mf = MutualFund(scheme_code=row["schemeCode"], scheme_name=row["schemeName"])
        db.session.add(mf)
    db.session.commit()
    print("Done")


if __name__ == "__main__":
    app.run(debug=True)
