import streamlit as st

def render_footer(current_page_label: str):
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

    page_links = {
        "🏠 Home": "Home.py",
        "🤖 AutoApply": "pages/1_🤖_AutoApply.py",
        "🔎 JobMatcher": "pages/2_🔎_JobMatcher.py",
        "💼 CareerMatch": "pages/3_💼_CareerMatch.py",
        "📚 SkillBridge": "pages/4_📚_SkillBridge.py",
        "📝 ResumeBuilder": "pages/5_📝_ResumeBuilder.py",
        "🛠️ ATS TuneUp": "pages/6_🛠️_ATS_TuneUp.py"
    }

    page_links.pop(current_page_label, None)  # Remove the current page from the links

    github_url = "https://github.com/azrael-2704/opportune-jobMate"
    linkedin_url = "https://www.linkedin.com/in/anayachala/"
    gmail_url = "mailto:opportune.jobmate@gmail.com"

    st.divider()

    st.caption(
    "<p style='text-align:center'>🚀 <strong>Opportune: JobMate</strong> — an intelligent toolset for resume analysis, role matching, and job automation.</p>"
    "<p style='text-align:center'>Built with ❤️ using Streamlit, spaCy, RapidFuzz and GeminiAPI.</p>",
    unsafe_allow_html=True)

    st.divider()

    col_left, col_right = st.columns([0.4, 0.4])

    with col_left:
        st.markdown("#### 💻 Access the Repo")
        col_gi, col_gl = st.columns([0.1, 0.9], vertical_alignment="center", gap="small")
        st.write("")
        st.markdown("#### 📧 Contact Me", unsafe_allow_html=True)
        col_li, col_ll = st.columns([0.1, 0.99], vertical_alignment="center", gap="small")
        col_ii, col_il = st.columns([0.1, 0.99], vertical_alignment="center", gap="small")
        with col_gi:
            st.image("ui/assets/githublogo.png", width=20)
        with col_gl:
            st.link_button("GitHub", github_url, type="tertiary")
        with col_li:
            st.image("ui/assets/linkedinlogo.png", width=20)
        with col_ll:
            st.link_button("LinkedIn", linkedin_url, type="tertiary")
        with col_ii:
            st.image("ui/assets/gmaillogo.png", width=20)
        with col_il:
            #st.link_button("Gmail", gmail_url, type="tertiary")
            st.write("opportune.jobmate@gmail.com")


    with col_right:
        st.markdown("#### 🔗 Other Links")
        for i, (label, path) in enumerate(page_links.items()):
            st.page_link(path, label=label, use_container_width=True)
    
    st.divider()
    st.markdown("<p style='font-size: 12px; color: #888; text-align:center'>© 2025 Amartya Anayachala. All rights reserved.</p>", unsafe_allow_html=True)
    st.divider()