import streamlit as st # type: ignore
import ui.render_footer as footer
import spacy
import json
import preprocessor.parser as parser
from preprocessor.skills import extract_skills_fuzzy
from recommender.resources import learning_resources

#Page configuration
st.set_page_config(page_title="SkillBridge", page_icon="📚", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size = "large", icon_image= "ui/assets/logo.png")

# Header
st.image("ui/assets/header.png", use_container_width=True)
st.write("")
st.caption("<p style='text-align: center;'>An intelligent tool to analyze your resume, match job roles, and evaluate job descriptions — all in one place</p>", unsafe_allow_html=True)
st.divider()

# Sidebar configuration
st.sidebar.title("📚 SkillBridge")
st.sidebar.markdown("Identify skill gaps for specific job roles. Upload your resume and select a job role to see the skills you need to develop!")

# Main content
st.title("📚 SkillBridge")
st.caption("Find out where you stand — and what you need to learn to level up.")
st.divider()

resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# --- Load Job Roles ---
@st.cache_data
def load_job_roles():
    with open("data/dataset/job_to_skill.json", "r") as f:
        return json.load(f)

job_skills_map = load_job_roles()
available_roles = sorted(job_skills_map.keys())

# --- Resume Extraction and Analysis ---
if resume_file:
    with st.spinner("Analyzing your resume and extracting skills..."):
        if resume_file.type == "application/pdf":
            resume_text = parser.extract_text_from_pdf(resume_file.read())
        elif resume_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            resume_text = parser.extract_text_from_docx(resume_file.read())
        else:
            st.error("Unsupported file type. Please upload a PDF or DOCX.")
            st.stop()
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("SpaCy model 'en_core_web_sm' not found. Please install it by running: python -m spacy download en_core_web_sm")
            st.stop()

        resume_doc = nlp(resume_text)
        extracted_skills = set(extract_skills_fuzzy(resume_doc))

    # --- Role Selection ---
    st.divider()
    selected_role = st.selectbox("Select a target job role:", available_roles)
    if selected_role:
        required_skills = set(job_skills_map[selected_role])
        matched_skills = extracted_skills & required_skills
        missing_skills = required_skills - extracted_skills

        st.divider()
        st.markdown(f"## 🎯 Skill Match for: {selected_role}")
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(f"#### ✅ Matched Skills: <span style='font-weight:normal'>({len(matched_skills)}/{len(required_skills)})</span>", unsafe_allow_html=True)
        st.markdown("#### " + " ".join(f":green-badge[{skill}]" for skill in sorted(matched_skills)) or "_None_")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"#### 💡 Recommended Additional Skills: <span style='font-weight:normal'>({len(missing_skills)} skill{'s' if len(missing_skills) != 1 else ''})</span>", unsafe_allow_html=True)
        st.markdown("#### " + " ".join(f":blue-badge[{skill}]" for skill in sorted(missing_skills)) or "_None_")

        st.divider()
        if missing_skills:
            st.markdown("### 📚 Recommended Resources for Additional Skills")
            learning_resources(missing_skills)
        else:
            st.success("You're fully equipped for this role! 💼")
# Footer
footer.render_footer("📚 SkillBridge")