from pathlib import Path

from backend.services.resume_parser import extract_resume_text

UPLOAD_DIR = Path("backend/uploads")

for file_path in UPLOAD_DIR.iterdir():

    if file_path.suffix.lower() in [".pdf", ".docx"]:

        try:
            text = extract_resume_text(file_path)

            print("\nFile:", file_path.name)
            print("Characters extracted:", len(text))
            print("Preview:", text[:300])
            print("-" * 50)

        except Exception as error:
            print("Failed:", file_path.name, error)