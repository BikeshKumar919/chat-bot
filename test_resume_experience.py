from backend.services.candidate_matcher import (
    extract_candidate_experience
)

test_resumes = [
    "Java developer with 4 years of experience.",
    "Python developer with 3+ years of experience.",
    "Experience: 5 years",
    "Experience - 4.5 years",
    "Fresher looking for an opportunity."
]

print("\nRESUME EXPERIENCE EXTRACTION")
print("-" * 50)

for resume in test_resumes:

    experience = extract_candidate_experience(resume)

    print(f"Resume: {resume}")
    print(f"Extracted Experience: {experience}")
    print("-" * 50)