
import re


# Skills our analyzer currently knows
SKILL_DATABASE = [
    "Java",
    "Spring Boot",
    "Spring Security",
    "REST APIs",
    "Microservices",
    "MySQL",
    "PostgreSQL",
    "Redis",
    "Kafka",
    "Docker",
    "Kubernetes",
    "Python",
    "React",
    "AWS",
    "Hibernate",
    "JPA",
    "Git"
]


def extract_job_title(job_description: str) -> str:
    """
    Extract the job title from the first line.
    """

    lines = [
        line.strip()
        for line in job_description.splitlines()
        if line.strip()
    ]

    return lines[0] if lines else "Not specified"


def extract_skills(job_description: str) -> list:
    """
    Identify known technical skills in the JD.
    """

    found_skills = []

    jd_lower = job_description.lower()

    for skill in SKILL_DATABASE:

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, jd_lower):
            found_skills.append(skill)

    return found_skills


def extract_experience(job_description: str):
    """
    Extract minimum years of experience.
    """

    patterns = [
        r"(\d+)\+?\s*years?\s+of\s+experience",
        r"minimum\s+(\d+)\s+years?",
        r"at\s+least\s+(\d+)\s+years?"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            job_description,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return None


def analyze_job_description(job_description: str) -> dict:
    """
    Analyze a job description and return structured data.
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty")

    skills_data = extract_required_and_preferred_skills(
    job_description
    )

    return {
    "job_title": extract_job_title(job_description),
    **skills_data,
    "minimum_experience_years": extract_experience(
        job_description
    ),
    "responsibilities": extract_responsibilities(
        job_description
    )
    }



def extract_required_and_preferred_skills(
    job_description: str
) -> dict:

    lines = job_description.splitlines()

    required_text = []
    preferred_text = []

    current_section = None

    for line in lines:

        line_lower = line.lower().strip()

        if "required skills" in line_lower:
            current_section = "required"
            continue

        if "preferred skills" in line_lower:
            current_section = "preferred"
            continue

        if line_lower.endswith(":"):
            current_section = None
            continue

        if current_section == "required":
            required_text.append(line)

        elif current_section == "preferred":
            preferred_text.append(line)

    required_skills = extract_skills(
        " ".join(required_text)
    )

    preferred_skills = extract_skills(
        " ".join(preferred_text)
    )

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills
    }



def extract_responsibilities(job_description: str) -> list:

    lines = job_description.splitlines()

    responsibilities = []
    inside_section = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        if "responsibilities" in line_lower:
            inside_section = True
            continue

        # Stop when another section starts
        if line_lower.endswith(":"):
            inside_section = False
            continue

        if inside_section:

            # Remove common bullet characters
            line = re.sub(r"^[\s•·\-*]+", "", line)

            if line:
                responsibilities.append(line)

    return responsibilities
