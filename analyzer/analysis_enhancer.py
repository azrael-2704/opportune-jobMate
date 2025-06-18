import streamlit as st
import google.generativeai as genai
import os
import json
import re

# Function to get API key from Streamlit secrets or user input
def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
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
            key="gemini_api_input_analysis" # Use a unique key for this file's API input
        )
        st.markdown(
            """
            <small><i>Note: The Gemini API has free tier usage limits (e.g., requests per minute, tokens per day). If you encounter errors like 'Quota Exceeded,' please wait a few minutes or check your usage on Google AI Studio.</i></small>
            """, unsafe_allow_html=True
        )
    return st.session_state.gemini_api_key

@st.cache_data(ttl=3600)
def list_available_gemini_models(api_key):
    if not api_key:
        return []
    try:
        genai.configure(api_key=api_key)
        models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models
    except Exception as e:
        if "API key not valid" not in str(e) and "Authentication error" not in str(e) and api_key:
            st.error(f"Error listing Gemini models: {e}. This might indicate a problem with your API key or network.")
        return []

def get_suitable_gemini_model(api_key):
    available_models = list_available_gemini_models(api_key)
    if not available_models:
        return None
    preferred_models_order = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest",
        "gemini-1.0-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-pro"
    ]
    selected_model = None
    for preferred_model_name in preferred_models_order:
        for model in available_models:
            if model.name == preferred_model_name or model.name == f"models/{preferred_model_name}":
                selected_model = model.name
                break
        if selected_model:
            break
    if selected_model:
        is_vision_only_model = "vision" in selected_model.lower() and not ("gemini-1.5-flash" in selected_model or "gemini-1.5-pro" in selected_model)
        if is_vision_only_model:
            for model in available_models:
                if 'generateContent' in model.supported_generation_methods and "vision" not in model.name.lower():
                    return model.name
            return selected_model
        else:
            return selected_model
    for model in available_models:
        if 'generateContent' in model.supported_generation_methods and "vision" not in model.name.lower():
            return model.name
    for model in available_models:
        if 'generateContent' in model.supported_generation_methods:
            return model.name
    return None

def generate_ats_analysis_prompt(resume_text, tone="Professional"):
    """
    Generates the prompt for ATS resume analysis, asking for JSON output.
    """
    return f"""
    As an expert ATS (Applicant Tracking System) and resume reviewer, analyze the following resume text for its ATS compatibility and overall professional quality.
    Provide a single overall ATS score out of 100, and a list of specific, actionable recommendations to improve the resume's ATS-friendliness and impact for any general job application.
    The analysis tone should be {tone}.

    Consider the following critical ATS and resume best practices:
    -   **Format & Layout:** Is it clean, standard (e.g., single column, standard fonts, minimal complex graphics/tables), and easily parsable? Avoid elements that might confuse ATS.
    -   **Keyword Density & Relevancy:** Is there a good density of relevant industry terminology (general, not job-specific)? Is it naturally integrated, or does it feel "stuffed"?
    -   **Conciseness & Length:** Are sections like summaries, responsibilities, and project descriptions appropriately sized? (e.g., summary 30-70 words, bullet points 1-2 sentences). Avoid overly long paragraphs or excessive bullet points (aim for 3-5 per role/project).
    -   **Quantifiable Achievements:** Does it include numbers, metrics, or specific results to demonstrate impact? If not, recommend adding them.
    -   **Missing Key Details:** Are essential sections like contact info, education, work experience, projects, and a professional summary present and complete? Are dates consistent?
    -   **Action Verbs:** Does it consistently use strong action verbs at the beginning of bullet points?
    -   **Readability & Clarity:** Is the language clear, professional, and easy for a human recruiter to skim and understand quickly?
    -   **Consistency:** Is formatting (fonts, dates, bullet styles) consistent throughout?

    Provide the response in the following JSON format ONLY, with no extra text or explanations:
    ```json
    {{
        "score": [INTEGER_SCORE_0_100],
        "recommendations": [
            "Recommendation 1 (e.g., 'Quantify achievements using numbers like X% or $Y.')",
            "Recommendation 2 (e.g., 'Ensure consistent date formats throughout the resume.')",
            "Recommendation 3 (e.g., 'Break down lengthy paragraphs into concise bullet points.')"
        ]
    }}
    ```
    Resume Text to Analyze:
    {resume_text}
    """

def perform_ats_analysis_ai(resume_text, tone, api_key):
    """
    Sends resume text to Google Gemini for ATS analysis and expects structured JSON.
    """
    if not api_key:
        st.error("Gemini API key is not provided. Please enter your API key to use AI enhancement.")
        return None

    model_name = get_suitable_gemini_model(api_key)
    if not model_name:
        st.error(f"No suitable Gemini model found for generation with your API key. Please check available models on Google AI Studio.")
        return None

    try:
        genai.configure(api_key=api_key)
        
        prompt = generate_ats_analysis_prompt(resume_text, tone)

        # Use response_mime_type in generation_config for JSON output hint
        response = genai.GenerativeModel(model_name).generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json" 
            },
            safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            }
        )
        
        if response and response.text:
            try:
                # Attempt to parse the JSON string
                parsed_json = json.loads(response.text)
                return parsed_json
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response from AI. The AI might not have returned valid JSON for ATS analysis.")
                st.markdown(f"Raw AI response (for debugging): \n```\n{response.text}\n```")
                return None # Return None or error object if parsing fails
        else:
            st.warning("AI analysis returned an empty or unexpected structured response for ATS analysis.")
            return None

    except Exception as e:
        error_message = str(e)
        if "API key not valid" in error_message or "Authentication error" in error_message:
            st.error("🚨 Gemini API Key Invalid: Please check your API key and try again.")
        elif "quota" in error_message or "rate limit" in error_message:
            st.error("🚨 Gemini API Quota Exceeded or Rate Limited: You've hit your usage limits. Please wait a few minutes and try again, or check your usage on [Google AI Studio](https://makersuite.google.com/app/apikey).")
        elif "404" in error_message and "models/" in error_message:
            st.error(f"🚨 Gemini Model Not Found or Not Supported: The model '{model_name}' might be unavailable or deprecated for your API key. Please try regenerating to select another suitable model or check Google AI Studio for available models.")
        else:
            st.error(f"🚨 An unexpected error occurred during AI analysis: {e}")
        return None

