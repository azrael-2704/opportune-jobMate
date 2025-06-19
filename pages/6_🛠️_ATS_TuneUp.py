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
run_local = col1.button("🔍 ATS Analysis", use_container_width=True)
run_ai = col2.button("✨ AI Enhanced Analysis", use_container_width=True)

if uploaded_file:
    resume_text = extract_text_from_uploaded_file(uploaded_file)

    if run_local:
        st.divider()
        st.subheader("🔍 ATS Analysis Results")
        st.write("")
        with st.spinner("Analyzing resume..."):
            local_feedback = run_local_ats_analysis(resume_text, uploaded_file)
            for step in local_feedback:
                st.markdown(f"### 🧩 Step {step['step']}: {step['title']}")
                for level, msg in step["findings"]:
                    if level == "warning":
                        st.warning(msg)
                    else:
                        st.success(msg)
            
            st.divider()
            st.write("")
            st.info("""We recommend the use of other online ATS Analysis tools as sometimes some tools provide new insights that the others do not. Some of the recommended tools are listed below:""")
            cols = st.columns([1, 1, 1], vertical_alignment='center', gap='small')
            with cols[0]:
                st.link_button("Weekday", "https://www.weekday.works/resume-checker-and-scoring-tool", use_container_width= True)
                st.link_button("MyPerfectResume", "https://www.myperfectresume.com/resume/ats-resume-checker", use_container_width= True)
            with cols[1]:
                st.link_button("Resume-Now", "https://www.resume-now.com/build-resume?mode=ats", use_container_width= True)
                st.link_button("Enhancv", "https://enhancv.com/resources/resume-checker/", use_container_width= True)
            with cols[2]:
                st.link_button("Jobscan", "https://www.jobscan.co/", use_container_width= True)
                st.link_button("1MillionResume", "https://1millionresume.com/resume-checker", use_container_width= True)

    elif run_ai:
        st.divider()
        if not api_key:
            st.error("Please enter your Google Gemini API key to use AI-based analysis.")
        else:
            st.subheader("✨ AI Enhanced ATS Analysis")
            st.write("")
            with st.spinner("AI is reviewing your resume..."):
                ai_feedback = perform_ai_ats_analysis(resume_text, api_key)

                # Display ATS score if present
                ats_score = ai_feedback.get("ATS_Score")
                if ats_score is not None:
                    st.markdown(f"### 🧠 ATS Compatibility Score: **{ats_score}/100**")
                    st.progress(min(int(ats_score), 100), text = "ATS Score")
                    if ats_score >= 80:
                        st.success("Excellent! Your resume is highly ATS-compatible.")
                    elif ats_score >= 60:
                        st.info("Good, but there's room for improvement.")
                    else:
                        st.warning("Needs improvement. Follow the suggestions below.")

                # Render all category feedback
                for category, results in ai_feedback.items():
                    if category == "ATS_Score":
                        continue
                    st.markdown(f"### 🎗️ {category}")
                    positives = results.get("Positives", [])
                    negatives = results.get("Negatives", [])
                    for pos in positives:
                        st.success(pos)
                    for neg in negatives:
                        st.warning(neg)
                
                st.divider()
                st.write("")
                st.info("""We recommend the use of other online ATS Analysis tools as sometimes some tools provide new insights that the others do not. Some of the recommended tools are listed below:""")
                cols = st.columns([1, 1, 1], vertical_alignment='center', gap='small')
                with cols[0]:
                    st.link_button("Weekday", "https://www.weekday.works/resume-checker-and-scoring-tool", use_container_width= True)
                    st.link_button("MyPerfectResume", "https://www.myperfectresume.com/resume/ats-resume-checker", use_container_width= True)
                with cols[1]:
                    st.link_button("Resume-Now", "https://www.resume-now.com/build-resume?mode=ats", use_container_width= True)
                    st.link_button("Enhancv", "https://enhancv.com/resources/resume-checker/", use_container_width= True)
                with cols[2]:
                    st.link_button("Jobscan", "https://www.jobscan.co/", use_container_width= True)
                    st.link_button("1MillionResume", "https://1millionresume.com/resume-checker", use_container_width= True)
else:
    st.info("Please upload your resume above to begin analysis.")

# Footer
footer.render_footer("🛠️ ATS TuneUp")