# Book Library ETL Pipeline

A Python project that enriches a CSV-based book catalog with cover images and presents the result through a Flask web application.

The project was built as a practical exercise in ETL workflow design, web scraping, file handling, data-quality checks, and lightweight web presentation.

## What the project does

The workflow starts with `books.csv`, which contains book metadata such as title, author, publication year, genre, and cover reference.

`web_scraper.py` reads the dataset, searches Open Library for missing cover images, downloads valid images to the local `static/covers` directory, and updates the CSV with the corresponding file names.

`repair_library.py` is a maintenance utility for removing empty cover files and clearing stale cover references.

`audit_library.py` provides a read-only quality report covering missing covers, duplicate titles, and image coverage.

`app.py` loads the enriched dataset and serves it through Flask. Jinja templates generate the book catalog dynamically, while books without a usable cover use a placeholder image.

## ETL Workflow

```text
books.csv
   |
   v
Pandas
   |
   v
Open Library search
   |
   v
Requests + BeautifulSoup
   |
   v
Cover validation and download
   |
   +----> static/covers/
   |
   v
Updated books.csv
   |
   v
Flask + Jinja
   |
   v
Web catalog
```

## Technologies

- Python
- Pandas
- Requests
- BeautifulSoup
- Flask
- Jinja2
- HTML / CSS
- pathlib

## Project Structure

```text
library-etl-flask/
|
|-- app.py
|-- web_scraper.py
|-- repair_library.py
|-- audit_library.py
|-- books.csv
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- templates/
|   `-- books.html
|
`-- static/
    `-- covers/
```

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the ETL

To retrieve missing covers and update the dataset:

```bash
python web_scraper.py
```

The scraper skips rows that already contain a cover reference.

If a usable cover cannot be retrieved, the value remains missing and the Flask application displays a placeholder image.

## Audit the Dataset

Run:

```bash
python audit_library.py
```

The audit reports:

- total book records
- cover coverage
- missing covers
- unique and repeated titles
- local image count
- books without a cover

The audit does not modify the dataset.

## Repair Local Cover Data

If a previous ETL run produced empty or stale local cover files:

```bash
python repair_library.py
```

This maintenance utility removes invalid local files and clears the corresponding cover references.

## Run the Flask Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The catalog is also available at:

```text
http://127.0.0.1:5000/books
```

## Data Quality

The pipeline does not force a cover match when one cannot be reliably retrieved.

A book may remain without a downloaded cover when:

- Open Library does not return a usable cover
- the returned image is a placeholder or unsupported URL
- a network request fails or times out
- the source dataset contains repeated records

Repeated titles in the source dataset are preserved rather than automatically removed.

## Open Library

The project uses HTML parsing because it originated as a practical exercise in web scraping.

For a production-oriented implementation, the cover retrieval step could be migrated to the official Open Library APIs.

## Possible Improvements

- Use the official Open Library API
- Cache repeated title lookups
- Match books using both title and author
- Add search and filtering to the Flask interface
- Move metadata storage from CSV to SQLite
- Add automated tests

## Project Scope

This is a small end-to-end learning project designed to demonstrate a complete workflow:

**extract external data → validate and transform → persist results → audit data quality → present through a web interface**
