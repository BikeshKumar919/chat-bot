from backend.services.candidate_matcher import (
    calculate_experience_score
)

required_years = 3

candidates = {
    "Candidate A": 5,
    "Candidate B": 3,
    "Candidate C": 2,
    "Candidate D": 1
}

print("\nEXPERIENCE MATCH RESULTS")
print("-" * 50)

for candidate, years in candidates.items():

    score = calculate_experience_score(
        years,
        required_years
    )

    print(
        f"{candidate}: {years} years | "
        f"Experience Score: {score}%"
    )