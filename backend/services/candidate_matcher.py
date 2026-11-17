import re


def contains_skill(text: str, skill: str) -> bool:

    pattern = (
        r"(?<!\w)"
        + re.escape(skill.lower())
        + r"(?!\w)"
    )

    return bool(re.search(pattern, text.lower()))


def calculate_skill_match(
    candidate_text: str,
    required_skills: list,
    preferred_skills: list
) -> dict:

    candidate_text_lower = candidate_text.lower()

    matched_required = []
    missing_required = []

    matched_preferred = []

    for skill in required_skills:

        if contains_skill(candidate_text_lower, skill):
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    for skill in preferred_skills:

        if contains_skill(candidate_text_lower, skill):
            matched_preferred.append(skill)

    required_score = (
        len(matched_required) / len(required_skills) * 100
        if required_skills else 0
    )

    preferred_score = (
        len(matched_preferred) / len(preferred_skills) * 100
        if preferred_skills else 0
    )

    return {
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "required_skill_score": round(required_score, 2),
        "preferred_skill_score": round(preferred_score, 2)
    }



def calculate_experience_score(
    candidate_years: float,
    required_years: float
) -> float:

    if required_years <= 0:
        return 100.0

    if candidate_years < 0:
        raise ValueError("Candidate experience cannot be negative")

    score = min(
        candidate_years / required_years,
        1.0
    ) * 100

    return round(score, 2)





def evaluate_candidate(
    candidate_text: str,
    required_skills: list,
    preferred_skills: list,
    required_years: float
) -> dict:

    skill_result = calculate_skill_match(
        candidate_text,
        required_skills,
        preferred_skills
    )

    experience = extract_candidate_experience(candidate_text)

    experience_score = None

    if experience is not None:
        experience_score = calculate_experience_score(
            experience,
            required_years
        )

    required_score = skill_result["required_skill_score"]
    preferred_score = skill_result["preferred_skill_score"]

    if experience_score is not None:

        overall_score = (
            required_score * 0.50
            + preferred_score * 0.15
            + experience_score * 0.35
        )

    else:
        overall_score = None

    return {
        **skill_result,
        "candidate_experience_years": experience,
        "required_experience_years": required_years,
        "experience_score": experience_score,
        "meets_minimum_experience": (
            experience >= required_years
            if experience is not None else None
        ),
        "overall_score": (
            round(overall_score, 2)
            if overall_score is not None else None
        )
    }



def extract_candidate_experience(candidate_text: str):

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            candidate_text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return None