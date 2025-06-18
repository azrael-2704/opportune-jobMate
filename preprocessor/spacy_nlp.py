import spacy
import streamlit as st

@st.cache_resource(ttl=3600)
def load_spacy_nlp_model(model_name="en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except Exception as e:
        st.error(f"Failed to load SpaCy model: {e}")
        st.stop()