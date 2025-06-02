import streamlit as st
from app.extractor import extract_text_from_pdf
from app.extractor import extract_keywords

st.title("Resume Analyzer - PDF Text Extractor")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract text
    extracted_text = extract_text_from_pdf("temp_resume.pdf")
    
    st.subheader("Extracted Text from PDF")
    st.text_area("", extracted_text, height = 400)

    # Extract keywords
    extracted_keywords = extract_keywords(extracted_text)
    st.subheader("Extracted Keywords")
    st.text_area("", extracted_keywords, height = 400)
