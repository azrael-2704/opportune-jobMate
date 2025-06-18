import streamlit as st
from ui import render_footer as footer
from analyzer.analysis_enhancer import (
    get_gemini_api_key,
    perform_ai_ats_analysis
)
from analyzer.resume_analysis import run_local_ats_analysis
from preprocessor.parser import extract_text_from_uploaded_file

# Page configuration
st.set_page_config(page_title="ATS TuneUp", page_icon="🛠️", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size="large", icon_image="ui/assets/logo.png")

# Header
st.image("ui/assets/header.png", use_container_width=True)
st.write("")
st.caption("<p style='text-align: center;'>An intelligent tool to analyze your resume, match job roles, and evaluate job descriptions — all in one place</p>", unsafe_allow_html=True)
st.divider()

# Sidebar
st.sidebar.title("ATS TuneUp")
st.sidebar.markdown("Analyze your resume for Applicant Tracking System (ATS) compatibility using expert-crafted rules and AI enhancement.")

# Title
st.title("🛠️ ATS TuneUp")
st.caption("Make your resume truly ATS-ready by identifying red flags and strengths with local rules or AI insights.")
st.divider()

# Upload Section
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
st.write("")

# AI Key Input Section
api_key = get_gemini_api_key()

# Buttons
col1, col2 = st.columns([1, 1])
run_local = col1.button("🔍 Local ATS Analysis", use_container_width=True)
run_ai = col2.button("✨ Gemini AI Analysis", use_container_width=True)

if uploaded_file:
    resume_text = extract_text_from_uploaded_file(uploaded_file)

    if run_local:
        st.divider()
        st.subheader("🔍 Local ATS Analysis Results")
        st.write("")
        with st.spinner("Analyzing resume with local rules..."):
            local_feedback = run_local_ats_analysis(resume_text, uploaded_file)
            for step in local_feedback:
                st.markdown(f"### 🧩 Step {step['step']}: {step['title']}")
                for level, msg in step["findings"]:
                    if level == "warning":
                        st.warning(msg)
                    else:
                        st.success(msg)

    elif run_ai:
        st.divider()
        if not api_key:
            st.error("Please enter your Google Gemini API key to use AI-based analysis.")
        else:
            st.subheader("✨ Gemini ATS Analysis Results")
            st.write("")
            with st.spinner("Gemini is reviewing your resume..."):
                ai_feedback = perform_ai_ats_analysis(resume_text, api_key)
                if ai_feedback:
                    for category, points in ai_feedback.items():
                        st.markdown(f"### 📌 {category}")
                        for p in points.get("Positives", []):
                            st.success(p)
                        for n in points.get("Negatives", []):
                            st.warning(n)
                else:
                    st.info("AI did not return structured feedback.")

else:
    st.info("Please upload your resume above to begin analysis.")

# Footer
footer.render_footer("🛠️ ATS TuneUp")