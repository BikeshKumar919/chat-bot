from pathlib import Path

from backend.services.resume_parser import extract_resume_text
from backend.services.candidate_matcher import evaluate_candidate
from backend.services.candidate_ranker import rank_candidates


def evaluate_all_candidates(
    upload_dir: Path,
    job: dict
) -> dict:

    results = []

    for file_path in upload_dir.iterdir():

        if file_path.suffix.lower() not in [".pdf", ".docx"]:
            continue

        try:
            resume_text = extract_resume_text(file_path)

            if not resume_text:
                raise ValueError("No text extracted from resume")

            evaluation = evaluate_candidate(
                candidate_text=resume_text,
                required_skills=job["required_skills"],
                preferred_skills=job["preferred_skills"],
                required_years=job["minimum_experience_years"] or 0
            )

            results.append({
                "candidate_id": file_path.stem,
                "filename": file_path.name,
                "status": "success",
                "evaluation": evaluation
            })

        except Exception as error:

            results.append({
                "candidate_id": file_path.stem,
                "filename": file_path.name,
                "status": "failed",
                "message": str(error)
            })

    ranking_result = rank_candidates(results)

    return {
        "total_processed": len(results),
        "successful": sum(
            1 for item in results
            if item["status"] == "success"
        ),
        "failed": sum(
            1 for item in results
            if item["status"] == "failed"
        ),
        **ranking_result
    }