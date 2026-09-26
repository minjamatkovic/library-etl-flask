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

DELETE_FILES = True


# -----------------------------------------------------------------------------
# Load dataset
# -----------------------------------------------------------------------------

df = pd.read_csv(BOOKS_FILE)

checked = 0
repaired = 0
deleted = 0


# -----------------------------------------------------------------------------
# Scan cover folder
# -----------------------------------------------------------------------------

for file in COVERS_DIR.iterdir():

    if not file.is_file():
        continue

    checked += 1

    # Obradjuj samo prazne fajlove
    if file.stat().st_size != 0:
        continue

    print(f"[WARNING] Empty file found: {file.name}")

    stem = file.stem

    # Pronađi tačno isti naziv fajla (bez ekstenzije)
    mask = (
        df["cover"]
        .fillna("")
        .apply(
            lambda x: Path(str(x)).stem == stem
        )
    )

    matches = mask.sum()

    if matches == 0:

        print(
            f"[WARNING] No CSV entry found for: {file.name}"
        )

    else:

        df.loc[mask, "cover"] = pd.NA

        repaired += matches

        print(
            f"[INFO] Cleared {matches} CSV record(s) "
            f"for {file.name}"
        )

    if DELETE_FILES:

        file.unlink()

        deleted += 1

        print(
            f"[INFO] Deleted: {file.name}"
        )


# -----------------------------------------------------------------------------
# Save
# -----------------------------------------------------------------------------

df.to_csv(
    BOOKS_FILE,
    index=False
)


# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------

print("\n----------------------------------------")
print("Library repair finished")
print("----------------------------------------")
print(f"Files checked : {checked}")
print(f"CSV repaired  : {repaired}")
print(f"Files deleted : {deleted}")
print("----------------------------------------")
    