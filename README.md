# AI Quiz Maker from Notes

Simple beginner-friendly project that turns lecture notes into practice quizzes.

Features
- Generates Multiple Choice Questions (MCQ), True/False statements, and Fill-in-the-blank questions.
- Uses NLTK for light NLP (tokenization, POS tagging) — no heavy ML models.
- Command-line interface: paste notes and receive a quiz printed + saved to JSON.

Project structure

ai_quiz_maker/
│── main.py            # CLI entry point
│── quiz_generator.py  # Quiz generation functions
│── utils.py           # Text cleaning & keyword extraction helpers
│── requirements.txt   # Python dependencies
│── README.md

Usage

1. Create a virtual environment (optional but recommended):

   python -m venv venv
   venv\Scripts\activate

2. Install requirements:

   pip install -r requirements.txt

3. Choose your interface:

   **Option A: GUI (Recommended for most users)**
   ```
   python gui.py
   ```
   - Opens a user-friendly window
   - Paste notes in the left panel
   - Click "Generate Quiz"
   - View questions in the right panel with tabs for MCQ, True/False, Fill-blank
   - Navigate with Previous/Next buttons
   - Export to JSON with a button click

   **Option B: Command-Line Interface**
   ```
   python main.py
   ```
   - Paste your notes into the terminal
   - After pasting, type a line with only `END` and press Enter

The program will print 5 MCQs, 5 True/False statements, and 5 Fill-in-the-blank questions
and save them to `quiz_output.json` in the current directory.

Notes
- The first run may download small NLTK data files (punkt, averaged_perceptron_tagger, stopwords).
- The generator uses simple heuristics: it extracts nouns as keywords and uses those
  to build questions and distractors. It is designed to be explainable and easy to read.

Extensions (optional)
- Export quiz to PDF or TXT
- Add randomized ordering or scoring/interactive quiz play
