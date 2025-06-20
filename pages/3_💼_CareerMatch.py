import streamlit as st # type: ignore
import ui.render_footer as footer
import ui. render_header as header
import preprocessor.parser as parser
from preprocessor.skills import extract_skills_fuzzy
import preprocessor.personal_info as pf
import recommender.top_n_jobs as jobRec
from preprocessor.spacy_nlp import load_spacy_nlp_model

#Page configuration
st.set_page_config(page_title="CareerMatch", page_icon="💼", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size = "large", icon_image= "ui/assets/logo.png")

# Header
header.render_header()

# Sidebar configuration
st.sidebar.title("💼 CareerMatch")
st.sidebar.markdown("Get the top job recommendations based on your resume skills. Upload your resume and let us find the best matches for you!")

# Main content
st.title("💼 Career Match")
st.caption("Upload your resume to get personalized job recommendations based on your skills and qualifications.")
st.divider()
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("Analyzing your resume and extracting information..."): # Updated spinner text
        file_type = uploaded_file.type  # MIME type

        if file_type == "application/pdf":
            extracted_text = parser.extract_text_from_pdf(uploaded_file.read())
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            extracted_text = parser.extract_text_from_docx(uploaded_file.read())
        elif file_type == "application/msword":  # This is .doc MIME type
            st.error("Sorry, .doc files are not supported. Please upload a PDF or DOCX file.")
            st.stop()
        else:
            st.error("Unsupported file type.")
            st.stop()

        nlp = load_spacy_nlp_model()
        
        doc = nlp(extracted_text)

        name = pf.extract_name(doc, extracted_text)
        email = pf.extract_mail(extracted_text)
        phone = pf.extract_phone(extracted_text)
        result = pf.extract_education_details(extracted_text)
        degree = result.get("degree") if result else None
        specialization = result.get("specialization") if result else None
        university = result.get("university") if result else None
        year = result.get("year") if result else None
        skills = sorted(extract_skills_fuzzy(doc))

    # Display extracted information
    st.divider()
    st.header("📄 Extracted Information")
    st.write("")
    
    st.markdown(f"##### 👤 Name: <span style='font-weight:normal'>{name if name else 'We couldn’t find your name — try adjusting your resume format.'}</span>", unsafe_allow_html=True)
    st.markdown(f"##### 📧 Email: <span style='font-weight:normal'>{email if email else 'We couldn’t locate your email — make sure it’s clearly written.'}</span>", unsafe_allow_html=True)
    st.markdown(f"##### 📱 Phone: <span style='font-weight:normal'>{phone if phone else 'We couldn’t identify your phone number — try formatting it clearly.'}</span>", unsafe_allow_html=True)
    st.markdown(f"##### 🗞️ Degree: <span style='font-weight:normal'>{degree.title() if degree else 'We couldn’t understand your degree — consider formatting it more clearly.'}</span>", unsafe_allow_html=True)
    st.markdown(f"##### 🧠 Specialization: <span style='font-weight:normal'>{specialization.title() if specialization else 'We couldn’t figure out your specialization — make sure it’s mentioned near your degree.'}</span>", unsafe_allow_html=True)
    st.markdown(f"##### 🏫 University: <span style='font-weight:normal'>{university.title() if university else 'We couldn’t identify your university — try writing the full name clearly.'}</span>", unsafe_allow_html=True)
    st.markdown(f"##### 🎓 Graduation Year: <span style='font-weight:normal'>{year if year else 'We couldn’t detect your graduation year — use a 4-digit format like 2020.'}</span>", unsafe_allow_html=True)

    st.write("")
    st.write(f"#### 💭 Skills:")
    st.markdown("#### " + " ".join(f":blue-badge[{skill}]" for skill in skills if skill))
    st.divider()

    st.write("Number of Job Recommendations:")
    topNJobs = st.slider("", min_value=1, max_value=20, value=5, key="topNJobs", label_visibility="collapsed")
    st.divider()
    
    with st.spinner("Finding suitable jobs for you..."):     
        recommended_jobs = jobRec.recommend_top_jobs(skills, topNJobs)
    
    # Display Suggestions
    st.markdown("## 🧭 Career Suggestions")
    st.markdown("<br>", unsafe_allow_html=True)
    if recommended_jobs:
        for job in recommended_jobs:
            st.markdown("### " + job['title'])
            st.markdown(f"##### Match Count: <span style='font-weight:normal'>{job['match_count']}</span>", unsafe_allow_html=True)
            st.markdown("##### Description:")
            if job.get("description"):
                st.markdown("###### " + f"<span style='font-weight:normal'>{job['description']}</span>", unsafe_allow_html=True)
            else:
                st.markdown("##### No description available.")
            st.markdown("##### Matched Skills:")
            st.markdown("#### " + " ".join(f":blue-badge[{skill}]" for skill in job['matched_skills']))
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.write("No jobs found matching your skills.")

# Footer
footer.render_footer("💼 CareerMatch")