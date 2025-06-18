import json
from collections import defaultdict

def recommend_top_jobs(resume_skills, top_n=5):
    skill_to_job_path = "data/dataset/skill_to_job.json"
    job_definitions_path = "data/dataset/job_definition.json"

    # Load data
    with open(skill_to_job_path, "r", encoding="utf-8") as f:
        raw_skill_to_job = json.load(f)
    with open(job_definitions_path, "r", encoding="utf-8") as f:
        job_descriptions = json.load(f)

    # Normalize keys in skill_to_job
    skill_to_job = {skill.lower(): job for skill, job in raw_skill_to_job.items()}

    # Score jobs
    job_scores = defaultdict(lambda: {"count": 0, "skills": []})
    for skill in resume_skills:
        matching_jobs = skill_to_job.get(skill.lower(), [])
        for job in matching_jobs:
            job_scores[job]["count"] += 1 # type: ignore
            job_scores[job]["skills"].append(skill) # type: ignore

    # Sort top jobs
    sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1]["count"], reverse=True)

    # Format result
    top_jobs = []
    for job, info in sorted_jobs[:top_n]:
        matched_skills = sorted(set(info["skills"])) # type: ignore
        descriptions = []

        # Split on slash and collect descriptions for each part
        parts = [j.strip() for j in job.split("/")]

        for part in parts:
            desc = job_descriptions.get(part)
            if desc:
                descriptions.append(f"<strong>{part}</strong>: {desc}")

        # Final description string
        if descriptions:
            full_description = "".join(f"<div style='padding-left: 20px; margin-bottom: 10px;'>{desc}</div>" for desc in descriptions)
        else:
            full_description = None

        top_jobs.append({
            "title": job,
            "match_count": info["count"],
            "matched_skills": matched_skills,
            "description": full_description
        })

    return top_jobs
