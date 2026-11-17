
from backend.services.job_analyzer import analyze_job_description


job_description = """
Java Backend Developer

We are looking for a Java Backend Developer
with at least 3 years of experience.

Required skills:
Java, Spring Boot, REST APIs, Microservices, MySQL.

Preferred skills:
Redis, Kafka, Docker.

Responsibilities:
Develop scalable backend services.
Design and implement REST APIs.
Work with microservice architecture.
Optimize database queries.
"""


result = analyze_job_description(job_description)

print("\nJOB ANALYSIS RESULT")
print("-" * 50)

for key, value in result.items():
    print(f"{key}: {value}")
