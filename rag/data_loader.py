# Name: Kofi Appiah
# Index: 10022300106
# File: rag/data_loader.py
# Purpose: Download and clean the datasets

import os
import requests
import pandas as pd
import fitz  # PyMuPDF
from tqdm import tqdm

# ── paths ──────────────────────────────────────────────
CSV_URL = "https://raw.githubusercontent.com/GodwinDansoAcity/acitydataset/main/Ghana_Election_Result.csv"
PDF_URL = "https://mofep.gov.gh/sites/default/files/budget-statements/2025-Budget-Statement-and-Economic-Policy_v4.pdf"

CSV_PATH = "data/ghana_elections.csv"
PDF_PATH = "data/budget_2025.pdf"
CLEAN_CSV_PATH = "data/clean_elections.txt"
CLEAN_PDF_PATH = "data/clean_budget.txt"


def download_file(url, save_path):
    """Download a file from a URL with a progress bar."""
    print(f"Downloading {save_path}...")
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))

    with open(save_path, 'wb') as f, tqdm(
        total=total, unit='B', unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))
    print(f"Saved to {save_path}")


def clean_csv():
    """Load and clean the elections CSV, return as plain text chunks."""
    print("Cleaning elections CSV...")
    df = pd.read_csv(CSV_PATH)

    # Drop empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # Strip whitespace from string columns
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

    # Convert each row to a readable sentence
    lines = []
    for _, row in df.iterrows():
        line = ", ".join(f"{col}: {val}" for col, val in row.items())
        lines.append(line)

    text = "\n".join(lines)

    with open(CLEAN_CSV_PATH, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Cleaned CSV saved → {CLEAN_CSV_PATH} ({len(lines)} rows)")
    return text


def clean_pdf():
    """Extract and clean text from the budget PDF."""
    print("Extracting budget PDF...")
    doc = fitz.open(PDF_PATH)
    pages = []

    for page in doc:
        text = page.get_text()
        # Remove excessive whitespace
        text = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )
        pages.append(text)

    full_text = "\n\n".join(pages)

    with open(CLEAN_PDF_PATH, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"Cleaned PDF saved → {CLEAN_PDF_PATH} ({len(pages)} pages)")
    return full_text


def load_data():
    """Main function — download and clean everything."""
    # Download if not already downloaded
    if not os.path.exists(CSV_PATH):
        download_file(CSV_URL, CSV_PATH)
    else:
        print(f"CSV already exists, skipping download.")

    if not os.path.exists(PDF_PATH):
        download_file(PDF_URL, PDF_PATH)
    else:
        print(f"PDF already exists, skipping download.")

    # Clean both
    csv_text = clean_csv()
    pdf_text = clean_pdf()

    return csv_text, pdf_text


if __name__ == "__main__":
    load_data()