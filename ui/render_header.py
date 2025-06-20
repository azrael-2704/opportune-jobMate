import streamlit as st

def render_header():
    st.image("ui/assets/header.png", use_container_width=True)
    st.write("")
    st.caption("<p style='text-align: center;'>An intelligent tool to analyze your resume, match job roles, and evaluate job descriptions — all in one place</p>", unsafe_allow_html=True)
    st.divider()