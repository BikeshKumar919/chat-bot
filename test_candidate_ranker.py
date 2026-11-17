from backend.services.candidate_ranker import rank_candidates

candidates = [
    {
        "candidate_id": "candidate1",
        "status": "success",
        "evaluation": {
            "overall_score": 75
        }
    },
    {
        "candidate_id": "candidate2",
        "status": "success",
        "evaluation": {
            "overall_score": 55
        }
    },
    {
        "candidate_id": "candidate3",
        "status": "success",
        "evaluation": {
            "overall_score": 35
        }
    },
    {
        "candidate_id": "candidate4",
        "status": "success",
        "evaluation": {
            "overall_score": None
        }
    }
]

result = rank_candidates(candidates)

print("\nCANDIDATE RANKING")
print("-" * 50)

for candidate in result["top_5"]:
    print(
        f"Rank: {candidate['rank']} | "
        f"ID: {candidate['candidate_id']} | "
        f"Score: {candidate['evaluation']['overall_score']}"
    )

print("\nCandidates needing review:")

for candidate in result["review_candidates"]:
    print(candidate["candidate_id"])