import streamlit as st  # type: ignore
from builder import form_inputs, generator_standard, enhancer
import ui.render_footer as footer
import re
from io import BytesIO
import time # Import the time module for delays

# Page configuration
st.set_page_config(page_title="ResumeBuilder", page_icon="📝", layout="centered", initial_sidebar_state="collapsed")
st.logo("ui/assets/header.png", size="large", icon_image="ui/assets/logo.png")

# Header
st.image("ui/assets/header.png", use_container_width=True)
st.write("")
st.caption("<p style='text-align: center;'>An intelligent tool to analyze your resume, match job roles, and evaluate job descriptions — all in one place</p>", unsafe_allow_html=True)
st.divider()

# Sidebar configuration
st.sidebar.title("📝 ResumeBuilder")
st.sidebar.markdown("Generate a professional resume tailored to your skills. Fill in your details and let us create a resume that stands out!")

# Main content
st.title("📝 ResumeBuilder")
st.caption("Generate your own ATS-friendly resume. Let AI add the powerful twist for interview success.")
st.divider()

# Step 1: Ask how many entries user wants to give
st.header("📌 Entry Counts for Sections")
st.write("")
col1, col2 = st.columns([1, 1], gap="small", vertical_alignment="center")
with col1:
    num_edu = st.number_input("How many education entries?", 0, 10, 1, key="edu_count")
    num_proj = st.number_input("How many projects?", 0, 10, 1, key="proj_count")
with col2:
    num_exp = st.number_input("How many work experiences?", 0, 10, 1, key="exp_count")
    num_cert = st.number_input("How many certifications?", 0, 10, 1, key="cert_count")
st.divider()

# Gemini API Key Input and Tone Control
st.header("🤖 AI Enhancement Options")
st.write("")
gemini_api_key = enhancer.get_gemini_api_key() # Get API key using the enhancer module
st.write("")
selected_tone = st.selectbox(
    "Select Enhancement Tone:",
    ["Professional", "Executive", "Technical", "Creative"],
    key="ai_tone_select",
    help="Choose the tone for AI-enhanced sections (Summary, Responsibilities, Projects, Skills, Achievements)."
)
st.divider()

# Step 2: Display dynamic form based on counts
st.header("✒️ Your Details")
st.write("")
with st.form("resume_form"):
    personal = form_inputs.personal_section()
    summary = form_inputs.summary_section()
    education = form_inputs.education_section(num_edu) if num_edu > 0 else []
    experience = form_inputs.experience_section(num_exp) if num_exp > 0 else []
    projects = form_inputs.project_section(num_proj) if num_proj > 0 else []
    skills = form_inputs.skills_section()
    certifications = form_inputs.certification_section(num_cert) if num_cert > 0 else []
    extras = form_inputs.additional_section()

    col_buttons = st.columns(2)
    with col_buttons[0]:
        generate_standard = st.form_submit_button("✅ Generate Resume", use_container_width=True)
    with col_buttons[1]:
        generate_ai_enhanced = st.form_submit_button("✨ Generate AI-Enhanced Resume", use_container_width=True)

# Step 3: Validation logic before rendering resume
if generate_standard or generate_ai_enhanced:
    errors = []
    warnings = []

    # Required field validation
    if not personal["name"].strip():
        errors.append("❌ Full Name is required.")
    if not personal["email"].strip():
        errors.append("❌ Email is required.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", personal["email"]):
        errors.append("❌ Email format is invalid.")
    if not personal["phone"].strip():
        errors.append("❌ Phone Number is required.")
    if not personal["location"].strip():
        warnings.append("⚠️ Adding your Location is recommended.")
    if not personal["linkedin"].strip():
        warnings.append("⚠️ Adding your LinkedIn URL is recommended.")
    if not personal["github"].strip():
        warnings.append("⚠️ Adding your GitHub URL is recommended.")
    if not personal["website"].strip():
        warnings.append("⚠️ Adding your Personal Website URL is recommended.")

    # Summary Check
    if not summary.strip():
        errors.append("❌ Professional Summary is required.")

    #Education Check
    for i in range (num_edu):
        if not education[i]["university"]:
            errors.append(f"❌ University {i + 1} is required.")
        if not education[i]["degree"]:
            errors.append(f"❌ Degree {i + 1} is required.")
        if not education[i]["end_date"]:
            errors.append(f"❌ End Date {i + 1} is required.")
        if not education[i]["gpa"]:
            warnings.append(f"⚠️ Adding your GPA {i + 1} is recommended.")
        if not education[i]["coursework"].strip():
            warnings.append(f"⚠️ Adding your Coursework {i + 1} is recommended.")

    # Work Experience Check
    for i in range (num_exp):
        if not experience[i]["job_title"]:
            errors.append(f"❌ Job Title {i + 1} is required.")
        if not experience[i]["company"]:
            errors.append(f"❌ Company {i + 1} is required.")
        if not experience[i]["end_date"]:
            errors.append(f"❌ Job End Date {i + 1} is required.")
        # Note: Responsibilities are handled differently now to ensure string format for generator.py
        if not experience[i]["responsibilities"]: # This will be a list from form_inputs
            warnings.append(f"⚠️ Adding your Job Responsibilities and Challenges {i + 1} is recommended.")
    
    # Project Check
    for i in range (num_proj):
        if not projects[i]["title"]:
            errors.append(f"❌ Project Title {i + 1} is required.")
        if not projects[i]["tech_stack"]:
            warnings.append(f"⚠️ Adding your Project Tech Stack {i + 1} is recommended.")
        if not projects[i]["link"]:
            warnings.append(f"⚠️ Adding your Repository Link {i + 1} is recommended.")
        if not projects[i]["deployment"]:
            warnings.append(f"⚠️ Adding your Deployment Link {i + 1} is recommended.")
        if not projects[i]["description"].strip(): # description is a string from form_inputs
            errors.append(f"❌ Project Description {i + 1} is required.")

    # Skills Check
    if len(skills["technical"]) + len(skills["soft"]) == 0:
        errors.append("❌ Please enter at least one skill (technical or soft).")
    elif len(skills["technical"]) <= 4:
        warnings.append("⚠️ Adding more Technical Skills is recommended.")
    elif len(skills["soft"]) <= 2:
        warnings.append("⚠️ Adding more Soft Skills is recommended.")
    
    # Certification Check
    for i in range (num_cert):
        if not certifications[i]["title"]:
            errors.append(f"❌ Certification Title {i + 1} is required.")
        if not certifications[i]["link"]:
            warnings.append(f"⚠️ Certification Link {i + 1} is recommended.")

    # Experience/project validation if count > 0
    if num_exp > 0 and not experience:
        errors.append("❌ You chose to add experience, but provided no entries.")
    if num_proj > 0 and not projects:
        errors.append("❌ You chose to add projects, but provided no entries.")

    # Display errors
    if errors and warnings:
        st.markdown("<br>", unsafe_allow_html=True)
        st.error("Please fix the following before generating your resume:\n\n" + "\n\n".join(f"{e}" for e in errors))
        st.write("")
        st.warning("Please consider adding the following for an ATS-friendly resume:\n\n" + "\n\n".join(f"{w}" for w in warnings))
    elif warnings: # This block is for when there are only warnings, allowing generation
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning("Please consider adding the following for an ATS-friendly resume:\n\n" + "\n\n".join(f"{w}" for w in warnings))
    elif errors: # Only errors, stop generation
        st.markdown("<br>", unsafe_allow_html=True)
        st.error("Please fix the following before generating your resume:\n\n" + "\n\n".join(f"{e}" for e in errors))
        st.stop() # Stop execution if there are errors

    if not errors:
        st.divider()

        # Wrap the AI enhancement block with st.spinner
        with st.spinner("AI is enhancing your resume... This might take a moment."):
            processed_personal = personal
            processed_summary = summary
            processed_education = education
            processed_skills = skills # Will be updated if AI enhanced
            processed_certifications = certifications
            processed_extras = extras # Will be updated if AI enhanced
            
            # Initialize processed_experience and processed_projects lists
            processed_experience = []
            processed_projects = []

            # Process Summary
            if generate_ai_enhanced and gemini_api_key:
                processed_summary = enhancer.enhance_content_with_gemini(
                    "professional summary", summary, selected_tone, gemini_api_key
                )
                time.sleep(3) # Add delay to respect API rate limits

            # Process Work Experience
            for i, exp_entry in enumerate(experience):
                current_exp = exp_entry.copy() # Create a copy to modify
                
                # Ensure responsibilities are processed consistently for generator_standard.py
                if generate_ai_enhanced and gemini_api_key:
                    enhanced_resp_text = enhancer.enhance_content_with_gemini(
                        "job responsibility", "\n".join(current_exp["responsibilities"]), selected_tone, gemini_api_key
                    )
                    # The enhancer now provides pure bullet points, one per line. Split by new line.
                    current_exp["responsibilities"] = [line.strip() for line in enhanced_resp_text.split('\n') if line.strip()] 
                elif isinstance(current_exp["responsibilities"], list):
                    current_exp["responsibilities"] = [r.strip() for r in current_exp["responsibilities"] if r.strip()] # Clean list elements
                
                processed_experience.append(current_exp)
                if generate_ai_enhanced and gemini_api_key:
                    time.sleep(3) # Add delay after each experience enhancement

            # Process Projects
            for i, proj_entry in enumerate(projects):
                current_proj = proj_entry.copy() # Create a copy to modify

                # Ensure description is processed consistently for generator_standard.py
                if generate_ai_enhanced and gemini_api_key:
                    enhanced_desc_text = enhancer.enhance_content_with_gemini(
                        "project description", current_proj["description"], selected_tone, gemini_api_key
                    )
                    # The enhancer now provides pure bullet points, one per line. Split by new line.
                    current_proj["description"] = [line.strip() for line in enhanced_desc_text.split('\n') if line.strip()]
                # If not AI enhanced, description is already a string from form_inputs.
                # If it was entered as multiple lines in the text area, it might already be split.
                # Ensure it's a list for consistency with enhanced output.
                elif isinstance(current_proj["description"], str):
                    current_proj["description"] = [line.strip() for line in current_proj["description"].split('\n') if line.strip()]

                processed_projects.append(current_proj)
                if generate_ai_enhanced and gemini_api_key:
                    time.sleep(3) # Add delay after each project enhancement

            # Process Skills
            if generate_ai_enhanced and gemini_api_key:
                # Combine technical and soft skills into a single string for enhancement
                all_skills_text = ", ".join(skills["technical"] + skills["soft"])
                enhanced_skills_string = enhancer.enhance_content_with_gemini(
                    "skills section", all_skills_text, selected_tone, gemini_api_key
                )
                # Parse the specific output format: "Technical Skills: ..., Soft Skills: ..."
                tech_skills = []
                soft_skills = []
                lines = enhanced_skills_string.split('\n')
                for line in lines:
                    if line.startswith("Technical Skills:"):
                        tech_str = line.replace("Technical Skills:", "").strip()
                        tech_skills = [s.strip() for s in tech_str.split(',') if s.strip()]
                    elif line.startswith("Soft Skills:"):
                        soft_str = line.replace("Soft Skills:", "").strip()
                        soft_skills = [s.strip() for s in soft_str.split(',') if s.strip()]
                
                processed_skills = {"technical": tech_skills, "soft": soft_skills}
                time.sleep(3) # Add delay after skills enhancement
            else:
                # Ensure skills are lists for generator, even if not enhanced
                processed_skills["technical"] = [s.strip() for s in processed_skills["technical"] if s.strip()]
                processed_skills["soft"] = [s.strip() for s in processed_skills["soft"] if s.strip()]


            # Process Achievements
            if generate_ai_enhanced and gemini_api_key:
                # Join all achievements into a single string for enhancement
                all_achievements_text = "\n".join(extras["achievements"])
                enhanced_achievements_string = enhancer.enhance_content_with_gemini(
                    "achievements", all_achievements_text, selected_tone, gemini_api_key
                )
                # The enhancer function is designed to return a comma-separated string for achievements
                # Convert back to a list
                processed_extras["achievements"] = [a.strip() for a in enhanced_achievements_string.split(',') if a.strip()]
                # No need for a final sleep if no more calls follow immediately
            else:
                # Ensure achievements are lists for generator, even if not enhanced
                processed_extras["achievements"] = [a.strip() for a in processed_extras["achievements"] if a.strip()]


        # Assemble data dictionary for generator (outside the spinner block, as processing is done)
        data = {
            "personal": processed_personal,
            "summary": processed_summary,
            "education": processed_education,
            "experience": processed_experience,
            "projects": processed_projects,
            "skills": processed_skills,
            "certifications": processed_certifications,
            "achievements_hobbies": processed_extras
        }

        # Generate and display resume
        try:
            docx_buffer = generator_standard.generate_structured_resume(data, "data/template.docx")
            
            if warnings:
                st.write("")
                st.success("Resume generated successfully!")
                st.info("Please note the following recommendations:\n\n" + "\n\n".join(f"{w}" for w in warnings))
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("Resume generated successfully!")

            #st.markdown("<br><br>", unsafe_allow_html=True)
            st.divider()
            st.write("")
            st.download_button(
                label="Download Resume (DOCX)",
                data=docx_buffer.getvalue(),
                file_name=f"{personal['name'].replace(' ', '_')}_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        except Exception as e:
            if warnings:
                st.write("")
                st.error(f"An error occurred during resume generation: {e}")
                st.info("This might be due to an issue with the template or data format. Please review your inputs or contact support.")
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.error(f"An error occurred during resume generation: {e}")
                st.info("This might be due to an issue with the template or data format. Please review your inputs or contact support.")

# Footer
footer.render_footer("📝 ResumeBuilder")