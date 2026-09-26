from pathlib import Path

import pandas as pd


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


# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------

df = pd.read_csv(BOOKS_FILE)


# -----------------------------------------------------------------------------
# Basic statistics
# -----------------------------------------------------------------------------

total_books = len(df)

books_without_cover = df["cover"].isna().sum()

books_with_cover = total_books - books_without_cover

unique_titles = df["title"].nunique()

duplicate_titles = total_books - unique_titles

image_count = len(
    [
        file
        for file in COVERS_DIR.iterdir()
        if file.is_file()
    ]
)

duplicate_cover_names = (
    df["cover"]
    .dropna()
    .duplicated()
    .sum()
)


# -----------------------------------------------------------------------------
# Duplicate titles
# -----------------------------------------------------------------------------

duplicate_title_table = (
    df["title"]
    .value_counts()
)

duplicate_title_table = duplicate_title_table[
    duplicate_title_table > 1
]


# -----------------------------------------------------------------------------
# Missing covers
# -----------------------------------------------------------------------------

missing_cover_titles = (
    df[df["cover"].isna()][
        ["title", "author"]
    ]
)


# -----------------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------------

print("\n")
print("=" * 60)
print("Library Audit")
print("=" * 60)

print(f"Books in CSV         : {total_books}")
print(f"Books with covers    : {books_with_cover}")
print(f"Books without covers : {books_without_cover}")

print()

print(f"Unique titles        : {unique_titles}")
print(f"Duplicate titles     : {duplicate_titles}")

print()

print(f"Images on disk       : {image_count}")
print(f"Duplicate cover names: {duplicate_cover_names}")

print("=" * 60)

print("\nTop duplicate titles:\n")

print(
    duplicate_title_table.head(20)
)

print("\n")

print("=" * 60)

print("Books without covers:\n")

if missing_cover_titles.empty:

    print("None")

else:

    print(
        missing_cover_titles.to_string(index=False)
    )

print("=" * 60)
