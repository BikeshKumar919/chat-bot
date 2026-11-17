def rank_candidates(candidates: list) -> dict:

    ranked_candidates = []
    review_candidates = []

    for candidate in candidates:

        if candidate["status"] != "success":
            review_candidates.append(candidate)
            continue

        evaluation = candidate["evaluation"]

        if evaluation["overall_score"] is None:
            review_candidates.append(candidate)
            continue

        ranked_candidates.append(candidate)

    ranked_candidates.sort(
        key=lambda item: item["evaluation"]["overall_score"],
        reverse=True
    )

    for rank, candidate in enumerate(ranked_candidates, start=1):
        candidate["rank"] = rank

    return {
        "total_ranked": len(ranked_candidates),
        "total_needing_review": len(review_candidates),
        "top_5": ranked_candidates[:5],
        "review_candidates": review_candidates
    }
