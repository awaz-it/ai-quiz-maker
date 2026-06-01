"""
Quick-start guide for the GUI version of AI Quiz Maker
"""

GUI_FEATURES = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                    AI QUIZ MAKER - GUI INTERFACE                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

WINDOW LAYOUT:
┌─────────────────────────────────────┬─────────────────────────────────────┐
│                                     │                                     │
│     LEFT PANEL:                     │     RIGHT PANEL:                    │
│     • Lecture Notes Input           │     • Quiz Display                  │
│     • ScrolledText widget           │     • Tab selection (MCQ, T/F, Fill)│
│     • Generate Button               │     • Question viewer               │
│     • Clear Button                  │     • Navigation arrows             │
│                                     │     • Export to JSON button         │
└─────────────────────────────────────┴─────────────────────────────────────┘

FEATURES:
========

1. NOTES INPUT AREA (Left Side)
   ✓ Large text box for pasting lecture notes
   ✓ Scroll bar for long notes
   ✓ "Generate Quiz" button to create questions
   ✓ "Clear" button to reset the input

2. QUIZ DISPLAY AREA (Right Side)
   ✓ Tab buttons: MCQ | True/False | Fill Blank
   ✓ Shows 1 question at a time with full details
   ✓ Navigate between questions with Previous/Next buttons
   ✓ Shows current position (e.g., "MCQ - Question 2 of 5")

3. MCQ QUESTIONS
   ✓ Question text displayed clearly
   ✓ All 4 options shown
   ✓ Correct answer highlighted in GREEN with ✓ mark
   ✓ Incorrect options in neutral background (for learning purposes)

4. TRUE/FALSE QUESTIONS
   ✓ Statement displayed prominently
   ✓ Answer shown in colored box:
     - GREEN for TRUE statements
     - RED for FALSE statements
   ✓ Clear, large "TRUE" or "FALSE" label

5. FILL-IN-THE-BLANK QUESTIONS
   ✓ Question with "_____" blank displayed
   ✓ Answer shown in blue box below
   ✓ Easy to read and understand

6. EXPORT FUNCTIONALITY
   ✓ "Export JSON" button saves quiz to file
   ✓ File dialog lets you choose save location
   ✓ Quiz saved in same format as CLI version

COLOR SCHEME:
=============
• Light gray background (#f0f0f0) - Main window
• White (#ffffff) - Input/Display areas
• Green (#4caf50) - Correct answers, TRUE statements
• Red (#f44336) - FALSE statements
• Blue (#1976d2) - Fill-blank answers
• Light blue (#e3f2fd) - Fill-blank answer box

KEYBOARD & MOUSE:
=================
✓ Click buttons to interact
✓ Type/Paste in notes area with Ctrl+V
✓ Scroll through long questions with mousewheel
✓ Tab between input and display areas

WORKFLOW:
=========
1. Run: python gui.py
2. Paste your lecture notes in the LEFT text box
3. Click "Generate Quiz"
4. View MCQ questions on the RIGHT side
5. Click "True/False" or "Fill Blank" tabs to see other question types
6. Use Previous/Next to navigate between questions
7. Click "Export JSON" to save the quiz

EXAMPLE OUTPUT:
===============

MCQ Question:
─────────────
"A router is a _____ device that forwards data packets between networks."

a) network (correct) ✓
b) storage
c) computing
d) display


True/False:
───────────
"Routers operate at Layer 3 of the OSI model."

Answer: TRUE  [GREEN BUTTON]


Fill-in-the-Blank:
──────────────────
"The Internet Protocol (IP) operates at the _____ layer."

Answer: Network

"""

print(GUI_FEATURES)
