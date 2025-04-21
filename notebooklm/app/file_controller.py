from sentence_transformers import SentenceTransformer
import faiss
import os
from app.models import ChatUrl, ChatFile
import torch
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import PyPDF2

# ------------------------- Content extraction functions -------------------------

def fetch_website_content(url):
    """
    Fetch content from a website URL.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract text from HTML
            raw_text = soup.get_text(separator="\n").strip()
            # Replace sequences of two or more whitespace characters with a single newline
            cleaned_text = re.sub(r'\s{2,}', '\n', raw_text)
            return cleaned_text
        else:
            return f"Error: Unable to fetch content (Status code: {response.status_code})"
    except Exception as e:
        return f"An error occurred while fetching content: {str(e)}"


def extract_pdf_content(file):
    """
    Extract text content from a PDF file.
    """
    try:
        # Open and read the PDF file
        reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in reader.pages)
        return text
    except Exception as e:
        return f"An error occurred while reading PDF: {str(e)}"


def extract_excel_content(file):
    """
    Extract content from an Excel file and convert it to markdown.
    """
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file)
        return df.to_markdown()  # Convert to markdown format
    except Exception as e:
        return f"An error occurred while reading Excel: {str(e)}"
