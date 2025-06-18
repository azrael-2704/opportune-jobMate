import streamlit as st
import spacy
from spacy.cli import download as spacy_download

@st.cache_resource(ttl=3600)
def load_spacy_nlp_model(model_name="en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        # Try to download it if not present
        try:
            st.info(f"Downloading SpaCy model '{model_name}'...")
            spacy_download(model_name)
            return spacy.load(model_name)
        except Exception as e:
            st.error(f"❌ Failed to load or download SpaCy model '{model_name}': {e}")
            st.stop()
