
from backend.services.semantic_search import search_resume_chunks

from backend.services.candidate_search_ranker import (
    rank_candidates_by_similarity
)


def search_and_rank_candidates(
    query: str,
    job_id: str
):
    # Step 1: Retrieve all chunks for this job
    search_results = search_resume_chunks(
        query=query,
        job_id=job_id,
        limit=None
    )

    # Step 2: Group chunks and rank candidates
    ranked_candidates = rank_candidates_by_similarity(
        search_results
    )

    return {
        "job_id": job_id,
        "total_chunks_matched": len(search_results),
        "total_candidates_found": len(ranked_candidates),
        "candidates": ranked_candidates
    }
