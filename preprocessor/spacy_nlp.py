import streamlit as st
import spacy
from spacy.cli import download as spacy_download

@st.cache_resource(ttl=3600)
def load_spacy_nlp_model(model_name="en_core_web_sm"):
    """
    Loads and caches a SpaCy NLP model.
    The model is loaded only once per Streamlit session due to st.cache_resource.
    """
    try:
        return spacy.load(model_name)
    except OSError:
        # If the model is not found (OSError), try to download it.
        st.error(f"SpaCy model '{model_name}' not found locally. Attempting to download...")
        with st.spinner(f"Downloading SpaCy model '{model_name}' (first time)... This may take a moment."):
            try:
                spacy_download(model_name)
                st.success(f"SpaCy model '{model_name}' downloaded successfully!")
                return spacy.load(model_name)
            except Exception as download_e:
                st.error(f"Failed to download SpaCy model '{model_name}': {download_e}")
                st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading SpaCy model '{model_name}': {e}")
        st.stop()