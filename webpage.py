from flask import Flask, render_template, request
from markupsafe import Markup
from interest import run

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart = None
    if request.method == "POST":
        base = float(request.form.get("base", ""))
        month = int(request.form.get("month", ""))
        year_rate = float(request.form.get("year_rate", ""))
        print(f"Input: base={base}, month={month}, year_rate={year_rate}")

        page = run(base, month, year_rate)
        chart = Markup(page.render_embed())

    return render_template("index.html", chart=chart)

if __name__ == "__main__":
    app.run(debug=True)
