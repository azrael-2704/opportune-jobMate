import streamlit as st
import os
import google.generativeai as genai
import json

def get_gemini_api_key():
    # Attempt to get from Streamlit secrets first (for deployment)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # If not in secrets, prompt user for it
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = ""

    with st.expander("🔑 **How to get your Google Gemini API Key**"):
        st.markdown(
            """
            1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
            2. Log in with your Google account.
            3. Click on "Create API key in new project" or copy an existing one.
            4. Paste your API key in the input box below.
            """
        )
        st.session_state.gemini_api_key = st.text_input(
            "Enter your Google Gemini API Key:",
            type="password",
            value=st.session_state.gemini_api_key,
            key="gemini_api_input"
        )
        st.markdown(
            """
            <small><i>Note: The Gemini API has free tier usage limits (e.g., requests per minute, tokens per day). If you encounter errors like 'Quota Exceeded,' please wait a few minutes or check your usage on Google AI Studio.</i></small>
            """, unsafe_allow_html=True
        )
    return st.session_state.gemini_api_key

def perform_ai_ats_analysis(text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    prompt = f"""
        You are an ATS resume expert. Analyze the resume below for the following categories:

        1. Contact Information
        2. Spelling & Grammar
        3. Personal Pronoun Usage
        4. Skills & Keyword Targeting
        5. Complex or Long Sentences
        6. Generic or Weak Phrases
        7. Passive Voice Usage
        8. Quantified Achievements
        9. Required Resume Sections
        10. AI-generated Language
        11. Repeated Action Verbs
        12. Visual Formatting or Readability
        13. Personal Information / Bias Triggers
        14. Other Strengths and Weaknesses

        Return your feedback strictly as JSON using this format:

        ```json
        {{
        "Contact Information": {{
            "Positives": ["..."],
            "Negatives": ["..."]
        }},
        ...
        }}
        Resume Text:
        {text}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Try to extract only the JSON block
        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1
        json_str = raw_text[json_start:json_end]

        parsed = json.loads(json_str)
        return parsed

    except Exception as e:
        st.error(f"❌ Gemini ATS Analysis Error: {e}")
        return {}
