
def rank_candidates_by_similarity(search_results: list) -> list:

    candidate_scores = {}

    for result in search_results:
        candidate_id = result["candidate_id"]
        similarity = 1 - result["distance"]

        if candidate_id not in candidate_scores:
            candidate_scores[candidate_id] = {
                "candidate_id": candidate_id,
                "best_similarity": similarity,
                "matching_chunks": []
            }

        candidate = candidate_scores[candidate_id]

        candidate["best_similarity"] = max(
            candidate["best_similarity"],
            similarity
        )

        candidate["matching_chunks"].append({
            "chunk_index": result["chunk_index"],
            "chunk_text": result["chunk_text"],
            "similarity": similarity
        })

    ranked_candidates = list(candidate_scores.values())

    ranked_candidates.sort(
        key=lambda item: item["best_similarity"],
        reverse=True
    )

    for rank, candidate in enumerate(ranked_candidates, start=1):
        candidate["rank"] = rank

    return ranked_candidates
