import streamlit as st
import ui.render_footer as footer
import ui.render_header as header

# Page configuration
st.set_page_config(page_title="Home", page_icon="🏠", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size = "large", icon_image= "ui/assets/logo.png")

# Sidebar configuration
st.sidebar.title("Home")
st.sidebar.markdown("Welcome to the Opportune: JobMate Landing Page! Use the sidebar to navigate through the tools available.")

# Header
header.render_header()

# Intro Section
st.title("👋 Welcome to Opportune: JobMate")
st.divider()
st.header("❔ What You Can Do")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([0.4, 0.6], vertical_alignment="center", gap="small")
col3, col4 = st.columns([0.4, 0.6], vertical_alignment="center", gap="small")
col5, col6 = st.columns([0.4, 0.6], vertical_alignment="center", gap="small")
col7, col8 = st.columns([0.4, 0.6], vertical_alignment="center", gap="small")
col9, col10 = st.columns([0.4, 0.6], vertical_alignment="center", gap="small")

with col1:
    st.page_link("pages/1_📡_JobRadar.py", label = "JobRadar", icon = "📡", use_container_width=True)
with col2:
    st.markdown("Finds job listings across multiple platforms in one place.")

with col3:
    st.page_link("pages/2_🔎_JobMatcher.py", label = "JobMatcher", icon = "🔎", use_container_width=True)
with col4:
    st.markdown("Checks if your resume fits a given Job Description.")

with col5:
    st.page_link("pages/3_💼_CareerMatch.py", label = "CareerMatch", icon = "💼", use_container_width=True)
with col6:
    st.markdown("Recommends top job roles based on your skills.")

with col5:
    st.page_link("pages/4_📚_SkillBridge.py", label = "SkillBridge", icon = "📚", use_container_width=True)
with col6:
    st.markdown("Identifies skill gaps for specific job roles.")

with col7:
    st.page_link("pages/5_📝_ResumeBuilder.py", label = "ResumeBuilder", icon = "📝", use_container_width=True)
with col8:
    st.markdown("Generates a professional resume tailored to your skills.")

with col9:
    st.page_link("pages/6_🛠️_ATS_TuneUp.py", label = "ATS TuneUp", icon = "🛠️", use_container_width=True)
with col10:
    st.markdown("Improve ATS compatibility and get resume enhancement tips.")

# Sidebar hint
st.markdown("---")
st.info("📂 Click on the required service or use the left sidebar to navigate between tools.")

# Footer
footer.render_footer("🏠 Home")