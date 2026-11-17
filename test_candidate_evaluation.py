from backend.services.candidate_matcher import evaluate_candidate

candidate_resume = """
Java Backend Developer

Experience: 4 years

Technical Skills:
Java, Spring Boot, Spring Security,
REST APIs, Microservices, MySQL,
Redis, Kafka.
"""

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

result = evaluate_candidate(
    candidate_text=candidate_resume,
    required_skills=required_skills,
    preferred_skills=preferred_skills,
    candidate_years=4,
    required_years=3
)

print("\nCANDIDATE EVALUATION")
print("-" * 50)

for key, value in result.items():
    print(f"{key}: {value}")