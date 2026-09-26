from pathlib import Path
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

BOOKS_FILE = BASE_DIR / "books.csv"

COVERS_DIR = (
    BASE_DIR
    / "static"
    / "covers"
)

HEADERS = {
    "User-Agent": (
        "LibraryETLFlask/1.0 "
        "(minja.zoran.matkovic@gmail.com)"
    )
}

REQUEST_TIMEOUT = 15


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def sanitize_filename(filename: str) -> str:
    """
    Convert a book title into a valid Windows filename.
    """

    filename = filename.lower().strip()

    filename = filename.replace(" ", "_")

    filename = re.sub(
        r'[<>:"/\\|?*]',
        "",
        filename
    )

    return filename


def normalize_image_url(image_source: str) -> str | None:
    """
    Normalize Open Library image URLs.
    Returns None if the URL is not a valid cover image.
    """

    if image_source.startswith("//"):
        return "https:" + image_source

    if image_source.startswith("https://"):
        return image_source

    return None


# -----------------------------------------------------------------------------
# Web scraping
# -----------------------------------------------------------------------------

def scrape_cover_image(title):

    try:

        query = title.replace(" ", "+")

        url = (
            f"https://openlibrary.org/search?q={query}"
        )

        response = requests.get(
            url=url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:

            print(f"[INFO] Search failed: {title}")

            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        book_cover = soup.find(class_="bookcover")

        if book_cover is None:

            print(f"[INFO] Cover not found: {title}")

            return None

        img_tag = book_cover.find("img")

        if img_tag is None:

            print(f"[INFO] Cover not found: {title}")

            return None

        image_source = img_tag.get("src")

        if not image_source:

            print(f"[INFO] Cover not found: {title}")

            return None

        image_source = normalize_image_url(image_source)

        if image_source is None:

            print(f"[INFO] Invalid cover URL: {title}")

            return None

        # Ignore placeholder icons
        if "avatar_book" in image_source:

            print(f"[INFO] Placeholder cover detected: {title}")

            return None

        cover_response = requests.get(
            image_source,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        if cover_response.status_code != 200:

            print(f"[INFO] Download failed: {title}")

            return None

        if len(cover_response.content) == 0:

            print(f"[INFO] Empty image: {title}")

            return None

        extension = image_source.split("?")[0].split(".")[-1]

        safe_title = sanitize_filename(title)

        file_name = (
            f"{safe_title}.{extension}"
        )

        cover_path = (
            COVERS_DIR
            / file_name
        )

        with open(
            cover_path,
            "wb"
        ) as file:

            file.write(
                cover_response.content
            )

        if cover_path.stat().st_size == 0:

            cover_path.unlink(missing_ok=True)

            print(f"[INFO] Empty file removed: {title}")

            return None

        print(f"[INFO] Cover found: {title}")

        return file_name

    except requests.exceptions.Timeout:

        print(f"[ERROR] Timeout: {title}")

        return None

    except requests.exceptions.RequestException as e:

        print(f"[ERROR] Request failed for {title}: {e}")

        return None

    except Exception as e:

        print(f"[ERROR] Unexpected error for {title}: {e}")

        return None


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

df = pd.read_csv(BOOKS_FILE)

downloaded = 0
skipped = 0
failed = 0

for index, row in df.iterrows():

    title = row["title"]
    author = row["author"]
    cover = row["cover"]

    if pd.notna(cover):

        print(
            f"[INFO] Book: "
            f"{title} - {author} "
            f"already has a cover. Skipping..."
        )

        skipped += 1

        continue

    print(
        f"[INFO] Searching cover for: "
        f"{title} - {author}"
    )

    image_title = scrape_cover_image(title)

    if image_title:

        df.at[index, "cover"] = image_title

        downloaded += 1

    else:

        failed += 1

    time.sleep(5)


df.to_csv(
    BOOKS_FILE,
    index=False
)

print("\n----------------------------------------")
print("Library ETL finished")
print("----------------------------------------")
print(f"Downloaded : {downloaded}")
print(f"Skipped    : {skipped}")
print(f"Failed     : {failed}")
print("----------------------------------------")
