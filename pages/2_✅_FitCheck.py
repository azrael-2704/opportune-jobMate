import streamlit as st
import spacy
import time # You can remove this import if time.sleep is no longer used anywhere else
import ui.render_footer as footer
import preprocessor.parser as parser
from preprocessor.skills import extract_skills_fuzzy, extract_soft_skills_fuzzy, weighted_skill_analysis
from recommender.resources import learning_resources

# Page configuration
st.set_page_config(page_title="FitCheck", page_icon="✅", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size="large", icon_image="ui/assets/logo.png")

# Header
st.image("ui/assets/header.png", use_container_width=True)
st.write("")
st.caption("<p style='text-align: center;'>An intelligent tool to analyze your resume, match job roles, and evaluate job descriptions — all in one place</p>", unsafe_allow_html=True)
st.divider()

# Sidebar
st.sidebar.title("FitCheck")
st.sidebar.markdown("Check if your resume fits a given Job Description. Upload your resume and the job description, and let us evaluate the compatibility!")

# Main title
st.title("✅ FitCheck")
st.caption("Analyze your resume against a job description to assess skill match, identify gaps, and measure compatibility.")
st.divider()

# Session state setup
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = 0
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

# Resume Upload
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
if resume_file:
    file_type = resume_file.type
    # It might be beneficial to put a small spinner here for file reading if files are very large
    # but for typical resumes, it's usually fast enough not to need it.
    if file_type == "application/pdf":
        st.session_state.resume_text = parser.extract_text_from_pdf(resume_file.read())
    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        st.session_state.resume_text = parser.extract_text_from_docx(resume_file.read())
    else:
        st.error("Unsupported file type.")
        st.stop()
st.divider()

# Tabs for JD input
tab_labels = ["📂 Upload Job Description", "✍️ Paste Job Description"]
selected_tab = st.radio("Choose Input Method", tab_labels, index=st.session_state.selected_tab, horizontal=True, )

# Reset if changed
if selected_tab != tab_labels[st.session_state.selected_tab]:
    st.session_state.selected_tab = tab_labels.index(selected_tab)
    st.rerun()

jd_text = None
if selected_tab == "📂 Upload Job Description":
    st.write("")
    jd_file = st.file_uploader("Upload the Job Description (PDF or DOCX)", type=["pdf", "docx"])
    if jd_file:
        jd_type = jd_file.type
        if jd_type == "application/pdf":
            jd_text = parser.extract_text_from_pdf(jd_file.read())
        elif jd_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            jd_text = parser.extract_text_from_docx(jd_file.read())
        else:
            st.error("Unsupported file type.")
            st.stop()

elif selected_tab == "✍️ Paste Job Description":
    st.write("")
    pasted_text = st.text_area("Paste the Job Description Here:", height=300)
    if pasted_text:
        jd_text = pasted_text

# Proceed if both inputs present
if st.session_state.resume_text and jd_text:
    st.divider()
    with st.spinner("Analyzing resume and job description..."): # More descriptive message
        # Removed time.sleep(1) here
        
        # Load spacy model
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("SpaCy model 'en_core_web_sm' not found. Please install it by running: python -m spacy download en_core_web_sm")
            st.stop()

        resume_doc = nlp(st.session_state.resume_text)
        jd_doc = nlp(jd_text)

        resume_hard = set(extract_skills_fuzzy(resume_doc))
        resume_soft = set(extract_soft_skills_fuzzy(resume_doc))
        jd_hard, jd_soft = weighted_skill_analysis(jd_text, nlp)

        def categorize(skills):
            core, imp, opt = [], [], []
            for s, w in skills.items():
                if w >= 2.5: core.append(s)
                elif w >= 1.0: imp.append(s)
                else: opt.append(s)
            return sorted(core), sorted(imp), sorted(opt)

        matched_hard = {s: w for s, w in jd_hard.items() if s in resume_hard}
        missing_hard = {s: w for s, w in jd_hard.items() if s not in resume_hard}
        matched_soft = jd_soft & resume_soft
        missing_soft = jd_soft - resume_soft

        total_w = sum(jd_hard.values())
        match_w = sum(matched_hard.values())
        hard_pct = (match_w / total_w) * 100 if total_w else 0
        soft_pct = (len(matched_soft) / len(jd_soft)) * 100 if jd_soft else 0

        hard_score = hard_pct * 0.9
        soft_score = soft_pct * 0.1
        final_score = round(hard_score + soft_score)

        c_m, i_m, o_m = categorize(matched_hard)
        c_x, i_x, o_x = categorize(missing_hard)

    # Display Results (outside the spinner)
    st.header("📊 FitCheck Score Breakdown")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### 🎯 Final Score: <span style='font-weight:normal'>{final_score}%</span>", unsafe_allow_html=True)
    st.markdown(f"### 🧱 Hard Skills Match: <span style='font-weight:normal'>{round(hard_pct)}% of 90 → {round(hard_score)} points</span>", unsafe_allow_html=True)
    st.markdown(f"### 🎭 Soft Skills Match: <span style='font-weight:normal'>{round(soft_pct)}% of 10 → {round(soft_score)} points</span>", unsafe_allow_html=True)
    st.write("")
    st.progress(final_score)
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    def show_skills(label, badge_color, skills):
        if skills:
            st.markdown(f"#### {label}: " + " ".join(f":{badge_color}-badge[{s}]" for s in skills))
        #else:
            #st.markdown(f"#### {label}: :gray-badge[_None_]")

    if matched_hard:
        st.subheader("✅ Matched Hard Skills")
        st.markdown("<br>", unsafe_allow_html=True)
        show_skills("🔐 Core Skills", "green", c_m)
        show_skills("💡 Important Skills", "green", i_m)
        show_skills("🧩 Nice-to-Have Skills", "green", o_m)

    if matched_soft:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("✅ Matched Soft Skills")
        st.markdown("<br>", unsafe_allow_html=True)
        show_skills("Soft Skills", "green", [s.title() for s in matched_soft])

    if missing_hard:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("❌ Missing Hard Skills")
        st.markdown("<br>", unsafe_allow_html=True)
        show_skills("🔐 Core Skills", "red", c_x)
        show_skills("💡 Important Skills", "red", i_x)
        show_skills("🧩 Nice-to-Have Skills", "red", o_x)

    if missing_soft:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("❌ Missing Soft Skills")
        st.markdown("<br>", unsafe_allow_html=True)
        show_skills("Soft Skills", "red", [s.title() for s in missing_soft])

    st.divider()
    if final_score > 80:
        st.success("✅ Excellent Match! You're highly compatible with this role.")
    elif final_score > 65:
        st.info("✨ Good Match! You're a solid fit. Consider upskilling slightly.")
    else:
        st.warning("⚠️ Needs Improvement. Upskilling recommended before applying.")

    # Learning resources
    st.divider()
    st.header("📚 Recommended Resources")
    st.write("")
    if missing_hard:
        skill_options = sorted(missing_hard.keys())
        learning_resources(skill_options)
    else:
        st.info("You've got all the hard skills covered!")

# Footer
footer.render_footer("✅ FitCheck")