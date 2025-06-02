import fitz  # PyMuPDF
import spacy

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_keywords(resume_text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(resume_text)
    keywords = [
        token.text for token in doc
        if token.pos_ in {"NOUN", "PROPN", "VERB"}
        and not token.is_stop
        and token.is_alpha
    ]
    return keywords
