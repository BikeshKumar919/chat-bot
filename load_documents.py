
from pathlib import Path

# Find the documents folder relative to this Python file
DOCUMENTS_DIR = Path(__file__).parent / "documents"

# Find all text files
text_files = list(DOCUMENTS_DIR.glob("*.txt"))

if not text_files:
    print("No .txt files found in the documents folder.")
else:
    print(f"Found {len(text_files)} document(s).\n")

    for file_path in text_files:
        text = file_path.read_text(encoding="utf-8")

        print("=" * 60)
        print("File:", file_path.name)
        print("Characters:", len(text))
        print("\nContent preview:\n")
        print(text[:500])
        print()
