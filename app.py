from pathlib import Path

import pandas as pd
from flask import Flask, render_template


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
BOOKS_FILE = BASE_DIR / "books.csv"


# -----------------------------------------------------------------------------
# Flask application
# -----------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/")
@app.route("/books")
def books():

    df = pd.read_csv(BOOKS_FILE)

    df["cover"] = df["cover"].fillna("")

    books = df.to_dict("records")

    return render_template(
        "books.html",
        books=books
    )


if __name__ == "__main__":
    app.run(debug=True)
