import streamlit as st # type: ignore
import ui.render_footer as footer

#Page configuration
st.set_page_config(page_title="AutoApply", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size = "large", icon_image= "ui/assets/logo.png")

# Header
st.image("ui/assets/header.png", use_container_width=True)
st.write("")
st.caption("<p style='text-align: center;'>An intelligent tool to analyze your resume, match job roles, and evaluate job descriptions — all in one place</p>", unsafe_allow_html=True)
st.divider()

# Sidebar configuration
st.sidebar.title("AutoApply")
st.sidebar.markdown("Automate the job application process by filling out forms. Upload your resume and let us handle the rest!")

# Main content
st.title("AutoApply")
st.caption("This feature is currently under development. Stay tuned for updates!")
st.divider()

# Footer
footer.render_footer("🤖 AutoApply")