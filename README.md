
![Opportune: JobMate](ui/assets/header.png)
---
A modular, intelligent resume analysis and enhancement platform.
---

## Overview  
Opportune: JobMate is a Streamlit-based suite for job seekers. It helps users analyze their resumes, match to job descriptions, enhance resume content, and prepare application-ready documents using NLP, AI, and resume intelligence. It supports both early-career professionals and experienced users seeking tailored job preparation tools.

---

## Modules and Functionality  

### 1. CareerMatch  
**Purpose**: Recommend ideal job roles based on resume skill analysis.

**Pipeline**:
- Parse resume (PDF/DOCX)
- Extract skills via NLP and fuzzy matching
- Canonicalize via `skills.json`
- Map to roles using `skill_to_job.json`
- Show matching job roles and role descriptions

### 2. JobSearch
**Purpose**: Analyze how well a resume fits a specific job description (JD).

**Pipeline**:
- Upload or paste a JD
- Heuristically segment sections (title, requirements, etc.)
- Weight each section's importance
- Match hard/soft skills against JD
- Provide compatibility score, missing skills, learning resources

### 3. SkillBridge  
**Purpose**: Compare resume skills with those needed for a selected job role.

**Pipeline**:
- Upload resume
- Select a role from `job_to_skills.json`
- Identify skill gaps
- Suggest resources for upskilling

### 4. ResumeBuilder  
**Purpose**: Form-based resume builder with AI-powered content enhancement.

**Features**:
- Ask number of entries per section
- Dynamically generate form inputs
- Render resume via Jinja2 or DOCX
- Optional Gemini API-based section rewording
- Export to HTML or DOCX
- Themes: Modern, Minimal, Harvard, Standard

### 5. ATS Tune-Up (Planned)  
Optimize resumes for ATS parsing by improving keyword targeting and structure.

### 6. AutoApply (Planned)  
Use browser automation to fill job forms on platforms like LinkedIn, Unstop, Glassdoor.

---

## Architecture

```
├── data/                     # Skill and job datasets
├── builder/                  # ResumeBuilder components
├── preprocessor/             # Resume + JD parsing
├── recommender/              # Role prediction logic
├── pages/                    # Streamlit multi-page UI
├── ui/                       # Footer, icons, styling
├── Home.py                   # App entrypoint
├── requirements.txt
├── README.md
```

---

## Key Technologies

- Python
- Streamlit
- spaCy (NLP)
- RapidFuzz (fuzzy matching)
- python-docx
- Google Gemini API (free tier)
- Jinja2 (resume templates)

---

## Data Sources and Attribution

We gratefully acknowledge the use of open datasets:

- Universities: [Kaggle – List of All Universities](https://www.kaggle.com/datasets/anshdwvdi/list-of-all-universities-in-the-world)
- IT Job Roles & Skills: [Kaggle – IT Roles Dataset](https://www.kaggle.com/datasets/dhivyadharunaba/it-job-roles-skills-dataset)
- Indian Colleges: [Kaggle – Top Indian Colleges](https://www.kaggle.com/datasets/soumyadipghorai/top-indian-colleges)

---

## Getting Started

```bash
pip install -r requirements.txt
streamlit run Home.py
```

---

## License  
MIT License © 2024  
Author: Amartya Anayachala