from backend.services.candidate_matcher import calculate_skill_match

# Sample resume text
candidate_resume = """
JavaScript Developer
Experience: 3 years


"""

# Job requirements
required_skills = [
    "Java",
    "Spring Boot",
    "REST APIs",
    "Microservices",
    "MySQL"
]

preferred_skills = [
    "Redis",
    "Kafka",
    "Docker"
]

result = calculate_skill_match(
    candidate_resume,
    required_skills,
    preferred_skills
)

print("\nCANDIDATE MATCH RESULT")
print("-" * 50)

for key, value in result.items():
    print(f"{key}: {value}")