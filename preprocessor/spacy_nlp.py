import streamlit as st
import spacy
from spacy.cli import download as spacy_download

def load_spacy_nlp_model(model_name="en_core_web_sm"):
    """
    Loads a SpaCy model, downloading it if not already available.
    """
    try:
        return spacy.load(model_name)
    except OSError:
        try:
            st.info(f"Downloading SpaCy model '{model_name}'...")
            spacy_download(model_name)
            return spacy.load(model_name)
        except Exception as e:
            st.error(f"❌ Failed to load or download SpaCy model '{model_name}': {e}")
            st.stop()
