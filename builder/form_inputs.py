import streamlit as st

def personal_section():
    with st.expander("👤 Personal Information"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone Number *")
        location = st.text_input("Location (Recommended)")
        linkedin = st.text_input("LinkedIn URL (Recommended)")
        github = st.text_input("GitHub URL (Recommended)")
        website = st.text_input("Portfolio Website (Recommended)")
        title = st.text_input("Professional Title")
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin": linkedin,
        "github": github,
        "website": website,
        "title": title
    }

def summary_section():
    with st.expander("📝 Summary"):
        summary = st.text_area("Professional Summary *")
    return summary

def education_section(count):
    entries = []
    for i in range(count):
        with st.expander(f"🎓 Education Entry {i + 1}"):
            entries.append({
                "degree": st.text_input(f"Degree *", key=f"edu_degree_{i}"),
                "university": st.text_input(f"University *", key=f"edu_uni_{i}"),
                "location": st.text_input(f"Location", key=f"edu_loc_{i}"),
                "start_date": st.text_input(f"Start Date", key=f"edu_sdate_{i}"),
                "end_date": st.text_input(f"End Date *", key=f"edu_edate_{i}"),
                "gpa": st.text_input(f"GPA (Recommended)", key=f"edu_gpa_{i}"),
                "coursework": st.text_area(f"Relevant Coursework (Recommended)", key=f"edu_course_{i}")
            })
    return entries

def experience_section(count):
    entries = []
    for i in range(count):
        with st.expander(f"💼 Work Experience {i + 1}"):
            entries.append({
                "job_title": st.text_input(f"Job Title *", key=f"exp_title_{i}"),
                "company": st.text_input(f"Company *", key=f"exp_company_{i}"),
                "location": st.text_input(f"Location", key=f"exp_loc_{i}"),
                "start_date": st.text_input(f"Start Date", key=f"exp_sdate_{i}"),
                "end_date": st.text_input(f"End Date *", key=f"exp_edate_{i}"),
                "responsibilities": st.text_area(f"Responsibilities (one per line) (Recommended)", key=f"exp_resp_{i}").splitlines()
            })
    return entries

def project_section(count):
    entries = []
    for i in range(count):
        with st.expander(f"🛠️ Project {i + 1}"):
            entries.append({
                "title": st.text_input(f"Project Title *", key=f"proj_title_{i}"),
                "tech_stack": st.text_input(f"Tech Stack (Recommended)", key=f"proj_tech_{i}"),
                "deployment": st.text_input(f"Deployment Link (Recommended)", key=f"proj_deploy_{i}"),
                "link": st.text_input(f"Project Link (Github Repo) (Recommended)", key=f"proj_link_{i}"),
                "description": st.text_area(f"Description *", key=f"proj_desc_{i}")
            })
    return entries

def skills_section():
    tech_skills = []
    soft_skills = []
    with st.expander("🧠 Skills"):
        hard_skills = st.text_area("Hard Skills (comma or line separated)").replace("\n", ",").split(",")
        soft_skills = st.text_area("Soft Skills (comma or line separated)").replace("\n", ",").split(",")
    return {
        "technical": [h.strip() for h in hard_skills if h.strip()],
        "soft": [s.strip() for s in soft_skills if s.strip()]
    }

def certification_section(count):
    entries = []
    for i in range(count):
        with st.expander(f"📜 Certification {i + 1}"):
            entries.append({
                "title": st.text_input(f"Certificate Title *", key=f"cert_title_{i}"),
                "issuer": st.text_input(f"Issued By", key=f"cert_issuer_{i}"),
                "link": st.text_input(f"Certificate Link (Recommended)", key=f"cert_link_{i}"),
            })
    return entries

def additional_section():
    with st.expander("🏆 Achievements & Hobbies"):
        achievements = st.text_area("Achievements (comma or line separated)").replace("\n", ",").split(",")
        hobbies = st.text_area("Hobbies (comma or line separated)").replace("\n", ",").split(",")
    return {
        "achievements": [a.strip() for a in achievements if a.strip()],
        "hobbies": [h.strip() for h in hobbies if h.strip()]
    }
