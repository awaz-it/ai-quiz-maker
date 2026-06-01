"""
gui.py

Tkinter GUI for the AI Quiz Maker from Notes.

This provides a professional, modern graphical interface where students can:
- Paste lecture notes
- Generate quizzes
- View MCQs, True/False, and Fill-in-the-blanks
- Navigate through questions
- Export quizzes as JSON

Features modern colors, buttons, hover effects, and professional design.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
from pathlib import Path

try:
    from quiz_generator import generate_mcq, generate_true_false, generate_fill_blank
except ImportError:
    from .quiz_generator import generate_mcq, generate_true_false, generate_fill_blank


# Professional Modern Color Palette
COLORS = {
    "primary": "#2563EB",        # Vibrant Blue
    "primary_hover": "#1D4ED8",  # Darker Blue
    "secondary": "#10B981",      # Emerald Green
    "secondary_hover": "#059669", # Darker Green
    "danger": "#EF4444",         # Red
    "danger_hover": "#DC2626",   # Darker Red
    "warning": "#F59E0B",        # Amber
    "warning_hover": "#D97706",  # Darker Amber
    "bg_light": "#F8FAFC",       # Light slate
    "bg_card": "#FFFFFF",        # White
    "text_primary": "#1E293B",   # Dark text
    "text_secondary": "#64748B", # Gray text
    "border": "#E2E8F0",         # Light border
    "success": "#10B981",        # Green
}


class ModernButton(tk.Canvas):
    """Custom button with rounded corners and smooth hover effects."""
    
    def __init__(self, parent, text="", emoji="", command=None, 
                 bg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                 width=140, height=45, **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height,
                          bg=COLORS["bg_light"], highlightthickness=0,
                          relief=tk.FLAT, bd=0, cursor="hand2", **kwargs)
        self.command = command
        self.text = text
        self.emoji = emoji
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hover = False
        self.width_val = width
        self.height_val = height
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", lambda e: self._draw_button())
    
    def _draw_button(self, hover=False):
        self.delete("all")
        color = self.hover_color if hover else self.bg_color
        
        # Draw rounded rectangle with gradient effect
        radius = 8
        w = self.winfo_width()
        h = self.winfo_height()
        
        # Draw arcs for corners
        self.create_arc(2, 2, 2+radius*2, 2+radius*2, start=90, extent=90,
                       fill=color, outline=color)
        self.create_arc(w-2-radius*2, 2, w-2, 2+radius*2, start=0, extent=90,
                       fill=color, outline=color)
        self.create_arc(w-2-radius*2, h-2-radius*2, w-2, h-2, start=270, extent=90,
                       fill=color, outline=color)
        self.create_arc(2, h-2-radius*2, 2+radius*2, h-2, start=180, extent=90,
                       fill=color, outline=color)
        
        # Fill rectangles
        self.create_rectangle(2+radius, 2, w-2-radius, h-2, fill=color, outline=color)
        self.create_rectangle(2, 2+radius, w-2, h-2-radius, fill=color, outline=color)
        
        # Draw text with emoji
        text_display = f"{self.emoji} {self.text}".strip() if self.emoji else self.text
        self.create_text(w/2, h/2, text=text_display, fill="white",
                        font=("Segoe UI", 10, "bold"), anchor="center")
    
    def _on_enter(self, event):
        self.is_hover = True
        self._draw_button(hover=True)
    
    def _on_leave(self, event):
        self.is_hover = False
        self._draw_button(hover=False)
    
    def _on_click(self, event):
        if self.command:
            self.command()


class CardFrame(tk.Frame):
    """Modern card with border and shadow effect."""
    
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, bg=COLORS["bg_card"], **kwargs)
        self.config(relief=tk.FLAT, borderwidth=1, highlightthickness=1,
                   highlightbackground=COLORS["border"], highlightcolor=COLORS["border"])


class QuizMakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Quiz Maker from Notes")
        self.root.geometry("1400x850")
        self.root.state('zoomed')  # Maximize window on startup (Windows)
        self.root.configure(bg=COLORS["bg_light"])
        
        # Data storage
        self.notes_text = ""
        self.current_quiz = None
        self.current_tab = "mcq"
        self.current_question_idx = 0
        
        self._create_widgets()
        self._update_question_display()
    
    def _create_widgets(self):
        """Create all GUI widgets with modern design."""
        # Create header
        self._create_header()
        
        # Main content area
        main_container = tk.Frame(self.root, bg=COLORS["bg_light"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel: Notes input
        left_panel = CardFrame(main_container, height=600)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Left panel title with icon
        left_title_frame = tk.Frame(left_panel, bg=COLORS["bg_card"])
        left_title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        left_title = tk.Label(left_title_frame, text="📝 Lecture Notes",
                             font=("Segoe UI", 16, "bold"), fg=COLORS["text_primary"],
                             bg=COLORS["bg_card"])
        left_title.pack(anchor=tk.W)
        
        left_subtitle = tk.Label(left_title_frame, text="Paste your lecture notes here",
                                font=("Segoe UI", 9), fg=COLORS["text_secondary"],
                                bg=COLORS["bg_card"])
        left_subtitle.pack(anchor=tk.W)
        
        # Notes text area with custom styling
        notes_frame = tk.Frame(left_panel, bg=COLORS["bg_card"])
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 15))
        
        self.notes_text_widget = scrolledtext.ScrolledText(
            notes_frame,
            height=20,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            bg=COLORS["bg_light"],
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            borderwidth=1,
            padx=12,
            pady=12,
            insertbackground=COLORS["primary"]
        )
        self.notes_text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Button frame with modern buttons - FIXED SIZE
        button_frame = tk.Frame(left_panel, bg=COLORS["bg_card"])
        button_frame.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Generate Quiz button - FIXED WIDTH
        generate_btn = ModernButton(
            button_frame,
            text="Generate Quiz",
            emoji="✨",
            command=self._generate_quiz,
            bg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            width=160,
            height=45
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10), expand=False)
        
        # Clear button - FIXED WIDTH
        clear_btn = ModernButton(
            button_frame,
            text="Clear",
            emoji="🗑️",
            command=self._clear_notes,
            bg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            width=130,
            height=45
        )
        clear_btn.pack(side=tk.LEFT, expand=False)
        
        # Right panel: Quiz display
        right_panel = CardFrame(main_container, height=600)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Right panel title with icon
        right_title_frame = tk.Frame(right_panel, bg=COLORS["bg_card"])
        right_title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        right_title = tk.Label(right_title_frame, text="🎯 Quiz Questions",
                              font=("Segoe UI", 16, "bold"), fg=COLORS["text_primary"],
                              bg=COLORS["bg_card"])
        right_title.pack(anchor=tk.W)
        
        right_subtitle = tk.Label(right_title_frame, text="Review and export your quiz",
                                 font=("Segoe UI", 9), fg=COLORS["text_secondary"],
                                 bg=COLORS["bg_card"])
        right_subtitle.pack(anchor=tk.W)
        
        # Tab selection with modern styling
        tab_frame = tk.Frame(right_panel, bg=COLORS["bg_card"])
        tab_frame.pack(fill=tk.X, padx=20, pady=(10, 15))
        
        tab_label = tk.Label(tab_frame, text="Question Type:",
                            font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"],
                            bg=COLORS["bg_card"])
        tab_label.pack(anchor=tk.W, pady=(0, 8))
        
        tabs_button_frame = tk.Frame(tab_frame, bg=COLORS["bg_card"])
        tabs_button_frame.pack(anchor=tk.W)
        
        self.tab_buttons = {}
        tab_configs = [
            ("mcq", "📋 MCQ", COLORS["primary"]),
            ("tf", "❓ True/False", COLORS["secondary"]),
            ("blank", "✏️ Fill Blank", COLORS["warning"])
        ]
        
        for tab_name, label, color in tab_configs:
            btn = ModernButton(
                tabs_button_frame,
                text=label.split()[1],
                emoji=label.split()[0],
                command=lambda t=tab_name: self._switch_tab(t),
                bg_color=color,
                hover_color=color if color == COLORS["primary"] else COLORS["secondary_hover"],
                width=115,
                height=40
            )
            btn.pack(side=tk.LEFT, padx=5, expand=False)
            self.tab_buttons[tab_name] = btn
        
        # Question display area
        question_label = tk.Label(right_panel, text="Question Display",
                                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_secondary"],
                                 bg=COLORS["bg_card"])
        question_label.pack(anchor=tk.W, padx=20, pady=(10, 5))
        
        self.question_frame = CardFrame(right_panel)
        self.question_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Navigation and info frame
        nav_frame = tk.Frame(right_panel, bg=COLORS["bg_card"])
        nav_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Question counter
        self.nav_label = tk.Label(nav_frame, text="No quiz generated",
                                 font=("Segoe UI", 10, "bold"), fg=COLORS["text_primary"],
                                 bg=COLORS["bg_card"])
        self.nav_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Navigation buttons - FIXED SIZE
        nav_buttons_frame = tk.Frame(nav_frame, bg=COLORS["bg_card"])
        nav_buttons_frame.pack(side=tk.LEFT, fill=tk.X)
        
        prev_btn = ModernButton(
            nav_buttons_frame,
            text="Previous",
            emoji="⬅️",
            command=self._previous_question,
            bg_color=COLORS["text_secondary"],
            hover_color=COLORS["text_primary"],
            width=130,
            height=40
        )
        prev_btn.pack(side=tk.LEFT, padx=3, expand=False)
        
        next_btn = ModernButton(
            nav_buttons_frame,
            text="Next",
            emoji="➡️",
            command=self._next_question,
            bg_color=COLORS["text_secondary"],
            hover_color=COLORS["text_primary"],
            width=130,
            height=40
        )
        next_btn.pack(side=tk.LEFT, padx=3, expand=False)
        
        # Export button on right - FIXED SIZE
        export_btn = ModernButton(
            nav_frame,
            text="Export",
            emoji="💾",
            command=self._export_quiz,
            bg_color=COLORS["success"],
            hover_color=COLORS["secondary_hover"],
            width=145,
            height=40
        )
        export_btn.pack(side=tk.RIGHT, expand=False)
    
    def _create_header(self):
        """Create professional header with gradient-like background."""
        header = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Header content frame
        header_content = tk.Frame(header, bg=COLORS["primary"])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Title with emoji
        title_label = tk.Label(header_content, text="📚 AI Quiz Maker from Notes",
                              font=("Segoe UI", 26, "bold"), fg="white", bg=COLORS["primary"])
        title_label.pack(anchor=tk.W)
        
        # Subtitle
        subtitle_label = tk.Label(header_content, text="Transform your lecture notes into interactive quizzes with AI",
                                 font=("Segoe UI", 11), fg="#E0E7FF", bg=COLORS["primary"])
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
    
    def _generate_quiz(self):
        """Generate quiz from the input notes."""
        notes = self.notes_text_widget.get("1.0", tk.END).strip()
        
        if not notes:
            messagebox.showwarning("Input Error", "Please paste lecture notes first.")
            return
        
        try:
            # Show progress
            messagebox.showinfo("Processing", "Generating quiz... This may take a moment.")
            
            mcqs = generate_mcq(notes, count=5)
            tfs = generate_true_false(notes, count=5)
            blanks = generate_fill_blank(notes, count=5)
            
            self.current_quiz = {
                "mcq": mcqs,
                "tf": tfs,
                "blank": blanks,
            }
            
            self.current_tab = "mcq"
            self.current_question_idx = 0
            self._update_question_display()
            messagebox.showinfo("Success", "✨ Quiz generated successfully!\n\nYou now have 5 MCQs, 5 True/False, and 5 Fill-in-the-blank questions.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate quiz:\n{str(e)}")
    
    def _switch_tab(self, tab_name):
        """Switch between quiz types."""
        if self.current_quiz is None:
            messagebox.showwarning("No Quiz", "Please generate a quiz first.")
            return
        
        self.current_tab = tab_name
        self.current_question_idx = 0
        self._update_question_display()
    
    def _clear_notes(self):
        """Clear the notes text area."""
        if messagebox.askyesno("Confirm", "Clear all notes?"):
            self.notes_text_widget.delete("1.0", tk.END)
    
    def _previous_question(self):
        """Go to previous question."""
        if self.current_quiz is None:
            return
        
        if self.current_question_idx > 0:
            self.current_question_idx -= 1
            self._update_question_display()
    
    def _next_question(self):
        """Go to next question."""
        if self.current_quiz is None:
            return
        
        questions = self.current_quiz[self.current_tab]
        if self.current_question_idx < len(questions) - 1:
            self.current_question_idx += 1
            self._update_question_display()
    
    def _update_question_display(self):
        """Update the question display area."""
        # Clear previous widgets
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        
        if self.current_quiz is None:
            empty_label = tk.Label(self.question_frame,
                                  text="📭 No quiz generated yet\n\nPaste your notes and click 'Generate Quiz'",
                                  font=("Segoe UI", 12), fg=COLORS["text_secondary"],
                                  bg=COLORS["bg_card"], justify=tk.CENTER)
            empty_label.pack(expand=True, pady=40)
            self.nav_label.config(text="No quiz generated")
            return
        
        questions = self.current_quiz[self.current_tab]
        if not questions:
            empty_label = tk.Label(self.question_frame,
                                  text="No questions available",
                                  font=("Segoe UI", 12), fg=COLORS["text_secondary"],
                                  bg=COLORS["bg_card"])
            empty_label.pack(expand=True, pady=40)
            return
        
        q = questions[self.current_question_idx]
        
        # Create scrollable frame for question content
        canvas = tk.Canvas(self.question_frame, bg=COLORS["bg_card"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.question_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_card"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Question type specific display
        if self.current_tab == "mcq":
            self._display_mcq(scrollable_frame, q)
        elif self.current_tab == "tf":
            self._display_true_false(scrollable_frame, q)
        elif self.current_tab == "blank":
            self._display_fill_blank(scrollable_frame, q)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Update navigation label
        total = len(questions)
        current = self.current_question_idx + 1
        tab_name = {"mcq": "MCQ", "tf": "True/False", "blank": "Fill Blank"}[self.current_tab]
        self.nav_label.config(text=f"{tab_name} • Question {current}/{total}")
    
    def _display_mcq(self, parent, question):
        """Display a multiple choice question."""
        # Question text
        q_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        q_frame.pack(fill=tk.X, padx=15, pady=(15, 20))
        
        q_label = tk.Label(
            q_frame,
            text=question["question"],
            font=("Segoe UI", 13, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg_card"],
            wraplength=500,
            justify=tk.LEFT
        )
        q_label.pack(anchor=tk.W)
        
        # Options
        options_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        options_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        correct_idx = question["answer"]
        
        for i, option in enumerate(question["options"]):
            letter = chr(ord('A') + i)
            is_correct = (i == correct_idx)
            
            # Color code: green for correct
            if is_correct:
                bg_color = "#D1FAE5"  # Light green
                border_color = COLORS["success"]
                text_color = "#065F46"  # Dark green
                text = f"{letter}. {option}  ✓"
            else:
                bg_color = COLORS["bg_light"]
                border_color = COLORS["border"]
                text_color = COLORS["text_primary"]
                text = f"{letter}. {option}"
            
            option_frame = tk.Frame(parent, bg=bg_color, relief=tk.FLAT, borderwidth=1)
            option_frame.pack(anchor=tk.W, fill=tk.X, pady=4, padx=15)
            
            inner_frame = tk.Frame(option_frame, bg=bg_color, padx=12, pady=10)
            inner_frame.pack(fill=tk.X)
            
            option_label = tk.Label(
                inner_frame,
                text=text,
                bg=bg_color,
                fg=text_color,
                font=("Segoe UI", 11),
                justify=tk.LEFT,
                wraplength=420,
                anchor=tk.W
            )
            option_label.pack(anchor=tk.W, fill=tk.X)
    
    def _display_true_false(self, parent, question):
        """Display a true/false question."""
        # Question text
        q_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        q_frame.pack(fill=tk.X, padx=15, pady=(15, 30))
        
        q_label = tk.Label(
            q_frame,
            text=question["statement"],
            font=("Segoe UI", 13, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg_card"],
            wraplength=500,
            justify=tk.LEFT
        )
        q_label.pack(anchor=tk.W)
        
        # Answer with color
        answer = question["answer"]
        if answer:
            answer_text = "TRUE"
            bg_color = "#D1FAE5"
            text_color = "#065F46"
            emoji = "✓"
        else:
            answer_text = "FALSE"
            bg_color = "#FEE2E2"
            text_color = "#7F1D1D"
            emoji = "✗"
        
        answer_frame = tk.Frame(parent, bg=bg_color, relief=tk.FLAT, borderwidth=1)
        answer_frame.pack(anchor=tk.W, fill=tk.X, padx=15, pady=(0, 15))
        
        inner_frame = tk.Frame(answer_frame, bg=bg_color, padx=15, pady=15)
        inner_frame.pack(fill=tk.X)
        
        answer_label = tk.Label(
            inner_frame,
            text=f"{emoji} Answer: {answer_text}",
            bg=bg_color,
            fg=text_color,
            font=("Segoe UI", 14, "bold")
        )
        answer_label.pack()
    
    def _display_fill_blank(self, parent, question):
        """Display a fill-in-the-blank question."""
        # Question text
        q_frame = tk.Frame(parent, bg=COLORS["bg_card"])
        q_frame.pack(fill=tk.X, padx=15, pady=(15, 30))
        
        q_label = tk.Label(
            q_frame,
            text=question["question"],
            font=("Segoe UI", 13, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["bg_card"],
            wraplength=500,
            justify=tk.LEFT
        )
        q_label.pack(anchor=tk.W)
        
        # Answer
        answer_frame = tk.Frame(parent, bg="#DBEAFE", relief=tk.FLAT, borderwidth=1)
        answer_frame.pack(anchor=tk.W, fill=tk.X, padx=15, pady=(0, 15))
        
        inner_frame = tk.Frame(answer_frame, bg="#DBEAFE", padx=15, pady=12)
        inner_frame.pack(fill=tk.X)
        
        answer_label = tk.Label(
            inner_frame,
            text=f"📝 {question['answer']}",
            bg="#DBEAFE",
            font=("Segoe UI", 12, "bold"),
            fg="#1E40AF"
        )
        answer_label.pack(anchor=tk.W)
    
    def _export_quiz(self):
        """Export the current quiz as TXT file."""
        if self.current_quiz is None:
            messagebox.showwarning("No Quiz", "Please generate a quiz first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="quiz_output.txt"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    # Write MCQs
                    f.write("=" * 80 + "\n")
                    f.write("MULTIPLE CHOICE QUESTIONS (MCQ)\n")
                    f.write("=" * 80 + "\n\n")
                    for i, q in enumerate(self.current_quiz["mcq"], 1):
                        f.write(f"Q{i}. {q['question']}\n")
                        for j, opt in enumerate(q["options"]):
                            letter = chr(ord('A') + j)
                            f.write(f"    {letter}. {opt}\n")
                        f.write(f"\nAnswer: {chr(ord('A') + q['answer'])}\n\n")
                    
                    # Write True/False
                    f.write("\n" + "=" * 80 + "\n")
                    f.write("TRUE / FALSE QUESTIONS\n")
                    f.write("=" * 80 + "\n\n")
                    for i, q in enumerate(self.current_quiz["tf"], 1):
                        f.write(f"Q{i}. {q['statement']}\n")
                        answer = "TRUE" if q["answer"] else "FALSE"
                        f.write(f"Answer: {answer}\n\n")
                    
                    # Write Fill-in-the-Blank
                    f.write("\n" + "=" * 80 + "\n")
                    f.write("FILL IN THE BLANK QUESTIONS\n")
                    f.write("=" * 80 + "\n\n")
                    for i, q in enumerate(self.current_quiz["blank"], 1):
                        f.write(f"Q{i}. {q['question']}\n")
                        f.write(f"Answer: {q['answer']}\n\n")
                
                messagebox.showinfo("Success", f"✅ Quiz exported successfully!\n\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")


def main():
    root = tk.Tk()
    app = QuizMakerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
