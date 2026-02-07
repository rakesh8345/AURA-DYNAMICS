# Attention Dynamics - Space Station Tech Division Edition
# UI/UX: Futuristic space station corporate aesthetic

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json

# Helper function to load data from JSON files
def load_data_from_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Data file not found: {filepath}")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Error decoding JSON from: {filepath}")
        return []






# ────────────────────────────────────────────────
#                   STYLE CONSTANTS
# ────────────────────────────────────────────────
COLOR_BG         = "#0a0e14"          # deep space black
COLOR_PANEL      = "#11171f"          # slightly lighter panel
COLOR_ACCENT     = "#00eaff"          # cyan neon
COLOR_ACCENT_DIM = "#00a3b7"          # dimmer cyan
COLOR_TEXT       = "#e0f7ff"          # light cyan-white
COLOR_TEXT_DIM   = "#a3c9d4"          # dimmer text
COLOR_CORRECT    = "#00ff9d"          # neon green
COLOR_WRONG      = "#ff3366"          # neon red
COLOR_BUTTON_BG  = "#1a2535"
COLOR_BUTTON_HL  = "#2a3b55"

FONT_TITLE  = ("Consolas", 18, "bold")
FONT_HEADER = ("Consolas", 22, "bold")
FONT_NORMAL = ("Consolas", 12)
FONT_BUTTON = ("Consolas", 13, "bold")
FONT_ITALIC = ("Consolas", 11, "italic")

# ────────────────────────────────────────────────
#                   MAIN APP
# ────────────────────────────────────────────────
class AttentionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATTENTION DYNAMICS // ORBITAL SOCIAL DIVISION v1.7")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(True, True)

        self.tips = load_data_from_json('tips.json')
        self.quiz_questions = load_data_from_json('quiz_questions.json')
        self.pda_questions = load_data_from_json('PDA.json')
        
        self.quiz_score = 0
        self.current_question_idx = 0
        self.selected_option = tk.IntVar(value=-1)
        self.pda_score = 0
        self.current_pda_question_idx = 0
        self.selected_pda_option = tk.IntVar(value=-1)
        self.current_pda_questions = []

        self.pda_option_map_rev = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        self.pda_option_map_fwd = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

        # ── Background canvas ──
        self.canvas = tk.Canvas(root, highlightthickness=0, bg=COLOR_BG)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)
        self.gradient_lines = [] # To store gradient lines for redrawing

        # ── Main container (frame for content) ──
        # This frame will be placed on top of the canvas
        main_frame = tk.Frame(root, bg=COLOR_PANEL, bd=1, relief="flat")
        # Use place with relx, rely, relwidth, relheight for proportional positioning
        # This creates a border around the main content that scales with the window
        main_frame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

        # Header
        tk.Label(main_frame, text="ORBITAL SOCIAL DYNAMICS TERMINAL", font=FONT_HEADER,
                 fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(pady=12)

        tk.Label(main_frame, text="Behavioral Analysis & Interpersonal Protocol Training System",
                 font=("Consolas", 10), fg=COLOR_TEXT_DIM, bg=COLOR_PANEL).pack(pady=(0,10))

        # Notebook with futuristic style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COLOR_PANEL, borderwidth=0)
        style.configure("TNotebook.Tab", background=COLOR_BUTTON_BG, foreground=COLOR_TEXT_DIM,
                        padding=[12,6], font=FONT_BUTTON)
        style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT_DIM)],
                  foreground=[("selected", COLOR_TEXT)])

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(pady=10, padx=15, fill="both", expand=True)

        # ── Tips Tab ──
        self.tip_frame = tk.Frame(self.notebook, bg=COLOR_PANEL)
        self.notebook.add(self.tip_frame, text=" PROTOCOLS ")

        tk.Label(self.tip_frame, text="Select protocol insight", font=FONT_NORMAL,
                 fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(pady=12)

        tk.Button(self.tip_frame, text="QUERY RANDOM PROTOCOL", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  activeforeground=COLOR_ACCENT, relief="flat", bd=1, width=28,
                  command=self.show_random_tip).pack(pady=8)

        self.tip_title_label = tk.Label(self.tip_frame, text="", font=("Consolas", 15, "bold"),
                                        fg=COLOR_ACCENT, bg=COLOR_PANEL, wraplength=620)
        self.tip_title_label.pack(pady=12)

        self.tip_desc_label = tk.Label(self.tip_frame, text="", font=FONT_NORMAL,
                                       fg=COLOR_TEXT, bg=COLOR_PANEL, wraplength=620, justify="left")
        self.tip_desc_label.pack(pady=4)

        self.tip_edu_label = tk.Label(self.tip_frame, text="", font=FONT_ITALIC,
                                      fg=COLOR_TEXT_DIM, bg=COLOR_PANEL, wraplength=620, justify="left")
        self.tip_edu_label.pack(pady=12)

        # ── Quiz Tab ──
        self.quiz_frame = tk.Frame(self.notebook, bg=COLOR_PANEL)
        self.notebook.add(self.quiz_frame, text=" EVALUATION ")

        # Frame for question selection controls (spinbox and start button)
        self.quiz_controls_frame = tk.Frame(self.quiz_frame, bg=COLOR_PANEL)
        self.quiz_controls_frame.pack(pady=(30, 0), padx=20, fill="x")

        tk.Label(self.quiz_controls_frame, text="Select number of questions:", font=FONT_NORMAL,
                 fg=COLOR_TEXT, bg=COLOR_PANEL).pack(pady=(0, 5))
        
        self.num_questions_var = tk.IntVar(value=min(20, len(self.quiz_questions)))
        self.num_questions_spinbox = ttk.Spinbox(self.quiz_controls_frame, from_=1, to=len(self.quiz_questions),
                                                 textvariable=self.num_questions_var, width=5,
                                                 font=FONT_NORMAL, state="readonly")
        self.num_questions_spinbox.pack(pady=5)

        self.start_quiz_button = tk.Button(self.quiz_controls_frame,
                                           text=f"INITIATE BEHAVIORAL EVALUATION ({len(self.quiz_questions)} CYCLES)",
                                           font=FONT_BUTTON, bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT,
                                           activebackground=COLOR_BUTTON_HL, relief="flat", bd=1, width=40,
                                           command=self.start_quiz)
        self.start_quiz_button.pack(pady=10) # Adjust padding as needed

        # Frame for displaying questions and results (this is the dynamic part)
        self.quiz_container = tk.Frame(self.quiz_frame, bg=COLOR_PANEL)
        self.quiz_container.pack(pady=(10, 30), padx=20, fill="both", expand=True)

        # ── PDA Tab ──
        self.pda_frame = tk.Frame(self.notebook, bg=COLOR_PANEL)
        self.notebook.add(self.pda_frame, text=" PDA ")

        # Frame for PDA controls (start button)
        self.pda_controls_frame = tk.Frame(self.pda_frame, bg=COLOR_PANEL)
        self.pda_controls_frame.pack(pady=(30, 0), padx=20, fill="x")

        tk.Label(self.pda_controls_frame, text="Personality Dynamics Analysis", font=FONT_NORMAL,
                 fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(pady=(0, 5))
        tk.Label(self.pda_controls_frame, text="This evaluation consists of 20 questions.", font=FONT_NORMAL,
                 fg=COLOR_TEXT_DIM, bg=COLOR_PANEL).pack(pady=(0, 10))

        self.start_pda_quiz_button = tk.Button(self.pda_controls_frame,
                                               text=f"INITIATE PDA EVALUATION (20 CYCLES)",
                                               font=FONT_BUTTON, bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT,
                                               activebackground=COLOR_BUTTON_HL, relief="flat", bd=1, width=40,
                                               command=self.start_pda_quiz)
        self.start_pda_quiz_button.pack(pady=10)

        # Frame for displaying PDA questions and results
        self.pda_container = tk.Frame(self.pda_frame, bg=COLOR_PANEL)
        self.pda_container.pack(pady=(10, 30), padx=20, fill="both", expand=True)



        # Status bar
        self.status_var = tk.StringVar(value="SYSTEM STANDBY | Awaiting input")
        tk.Label(root, textvariable=self.status_var, font=("Consolas", 10),
                 fg=COLOR_TEXT_DIM, bg=COLOR_BG, anchor="w").place(relx=0.03, rely=0.97, relwidth=0.7, anchor="sw")

        tk.Button(root, text="TERMINATE", font=FONT_BUTTON,
                  bg="#3a1a1a", fg="#ff4d4d", activebackground="#551111", relief="flat", bd=1, width=12,
                  command=root.quit).place(relx=0.97, rely=0.97, anchor="se")

    def _on_resize(self, event):
        # Redraw the subtle nebula-like gradient lines on resize
        self.canvas.delete("gradient_line") # Delete old lines

        width = event.width
        height = event.height

        # Redraw gradient lines to fill new canvas size
        for i in range(0, width, 40):
            self.canvas.create_line(i, 0, i + width // 6, height, fill="#0f1a2a", width=80, stipple="gray75", tags="gradient_line")

    def show_random_tip(self):
        tip = random.choice(self.tips)
        self.tip_title_label.config(text="► " + tip["title"])
        self.tip_desc_label.config(text=tip["description"])
        self.tip_edu_label.config(text="NEURO-PSYCH ANALYSIS: " + tip["education"])
        self.status_var.set("PROTOCOL RETRIEVED | Cycle complete")

    def start_quiz(self):
        try:
            num_selected_questions = self.num_questions_var.get()
            if not (1 <= num_selected_questions <= len(self.quiz_questions)):
                messagebox.showwarning("Invalid Input", f"Please select a number between 1 and {len(self.quiz_questions)}.")
                return
        except tk.TclError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number for questions.")
            return
        
        self.current_quiz_questions = random.sample(self.quiz_questions, num_selected_questions)

        self.quiz_score = 0
        self.current_question_idx = 0
        self.selected_option.set(-1)
        self.quiz_controls_frame.pack_forget() # Hide the entire controls frame
        self.show_question()

    def start_pda_quiz(self):
        self.pda_score = 0
        self.current_pda_question_idx = 0
        self.selected_pda_option.set(-1)
        
        # PDA quiz always has 20 questions
        if len(self.pda_questions) < 20:
            messagebox.showwarning("PDA Error", "Not enough PDA questions available (need 20).")
            return
        self.current_pda_questions = random.sample(self.pda_questions, 20)
        
        self.pda_controls_frame.pack_forget() # Hide the entire PDA controls frame
        self.show_pda_question()

    def show_question(self):
        for widget in self.quiz_container.winfo_children():
            widget.destroy()

        if self.current_question_idx >= len(self.current_quiz_questions):
            self.show_quiz_results()
            return

        q = self.current_quiz_questions[self.current_question_idx]

        tk.Label(self.quiz_container, text=f"CYCLE {self.current_question_idx+1}/{len(self.current_quiz_questions)}",
                 font=("Consolas", 12, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(anchor="w", pady=6)

        tk.Label(self.quiz_container, text=q["question"], font=FONT_NORMAL,
                 fg=COLOR_TEXT, bg=COLOR_PANEL, wraplength=620, justify="left").pack(anchor="w", pady=12)

        for i, option in enumerate(q["options"]):
            rb = tk.Radiobutton(self.quiz_container, text=option, variable=self.selected_option, value=i,
                                font=FONT_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXT,
                                selectcolor=COLOR_PANEL, activebackground=COLOR_PANEL,
                                activeforeground=COLOR_ACCENT)
            rb.pack(anchor="w", pady=4)

        tk.Button(self.quiz_container, text="SUBMIT RESPONSE", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  relief="flat", bd=1, width=25,
                  command=self.check_answer).pack(pady=25)

    def show_pda_question(self):
        for widget in self.pda_container.winfo_children():
            widget.destroy()

        if self.current_pda_question_idx >= len(self.current_pda_questions):
            self.show_pda_results()
            return

        q = self.current_pda_questions[self.current_pda_question_idx]

        tk.Label(self.pda_container, text=f"PDA CYCLE {self.current_pda_question_idx+1}/{len(self.current_pda_questions)}",
                 font=("Consolas", 12, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(anchor="w", pady=6)

        tk.Label(self.pda_container, text=q["question"], font=FONT_NORMAL,
                 fg=COLOR_TEXT, bg=COLOR_PANEL, wraplength=620, justify="left").pack(anchor="w", pady=12)
        
        self.pda_option_map_rev = {'A': 0, 'B': 1, 'C': 2, 'D': 3} # Map for converting letter to int for radiobutton value
        self.pda_option_map_fwd = {0: 'A', 1: 'B', 2: 'C', 3: 'D'} # Map for converting int back to letter for checking

        for letter, text in q["options"].items():
            rb = tk.Radiobutton(self.pda_container, text=f"{letter}. {text}", variable=self.selected_pda_option, value=self.pda_option_map_rev[letter],
                                font=FONT_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXT,
                                selectcolor=COLOR_PANEL, activebackground=COLOR_PANEL,
                                activeforeground=COLOR_ACCENT)
            rb.pack(anchor="w", pady=4)

        tk.Button(self.pda_container, text="SUBMIT PDA RESPONSE", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  relief="flat", bd=1, width=25,
                  command=self.check_pda_answer).pack(pady=25)

    def check_answer(self):
        if self.selected_option.get() == -1:
            messagebox.showwarning("INPUT REQUIRED", "Please select response vector.")
            return

        q = self.current_quiz_questions[self.current_question_idx]
        is_correct = self.selected_option.get() == q["correct"]

        if is_correct:
            self.quiz_score += 1
            feedback = f"POSITIVE RESPONSE CONFIRMED ✓\n\n{q['explanation']}"
            color = COLOR_CORRECT
        else:
            feedback = f"NEGATIVE MATCH\nCorrect vector: {q['options'][q['correct']]}\n\n{q['explanation']}"
            color = COLOR_WRONG

        for widget in self.quiz_container.winfo_children():
            widget.destroy()

        tk.Label(self.quiz_container, text=feedback, font=FONT_NORMAL,
                 fg=color, bg=COLOR_PANEL, wraplength=620, justify="left").pack(pady=15)

        tk.Button(self.quiz_container, text="NEXT CYCLE", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  relief="flat", bd=1, width=25,
                  command=self.next_question).pack(pady=20)

    def check_pda_answer(self):
        if self.selected_pda_option.get() == -1:
            messagebox.showwarning("INPUT REQUIRED", "Please select response vector.")
            return

        q = self.current_pda_questions[self.current_pda_question_idx]
        selected_letter = self.pda_option_map_fwd[self.selected_pda_option.get()]
        is_correct = (selected_letter == q["correct"])

        if is_correct:
            self.pda_score += 1
            feedback = f"POSITIVE RESPONSE CONFIRMED ✓\n\nCorrect choice: {selected_letter}. {q['options'][q['correct']]}"
            color = COLOR_CORRECT
        else:
            feedback = f"NEGATIVE MATCH\nCorrect choice: {q['correct']}. {q['options'][q['correct']]}"
            color = COLOR_WRONG

        for widget in self.pda_container.winfo_children():
            widget.destroy()

        tk.Label(self.pda_container, text=feedback, font=FONT_NORMAL,
                 fg=color, bg=COLOR_PANEL, wraplength=620, justify="left").pack(pady=15)

        tk.Button(self.pda_container, text="NEXT PDA CYCLE", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  relief="flat", bd=1, width=25,
                  command=self.next_pda_question).pack(pady=20)

    def next_question(self):
        self.current_question_idx += 1
        self.selected_option.set(-1)
        self.show_question()

    def next_pda_question(self):
        self.current_pda_question_idx += 1
        self.selected_pda_option.set(-1)
        self.show_pda_question()

    def show_quiz_results(self):
        # Check if current_quiz_questions is empty to avoid division by zero
        if not self.current_quiz_questions:
            percent = 0
            num_answered = 0
            total_questions_in_quiz = 0
        else:
            total_questions_in_quiz = len(self.current_quiz_questions)
            num_answered = self.quiz_score
            percent = (num_answered / total_questions_in_quiz) * 100

        msg = f"EVALUATION COMPLETE\n\nSCORE: {num_answered}/{total_questions_in_quiz}  ({percent:.1f}%)\n\n"

        if percent >= 85:
            msg += "EXCELLENT PROTOCOL MASTERY — Subject shows high social calibration"
        elif percent >= 60:
            msg += "ACCEPTABLE PERFORMANCE — Further training recommended"
        else:
            msg += "SIGNIFICANT RECALIBRATION REQUIRED"

        for widget in self.quiz_container.winfo_children():
            widget.destroy()

        tk.Label(self.quiz_container, text=msg, font=("Consolas", 14, "bold"),
                 fg=COLOR_ACCENT, bg=COLOR_PANEL, wraplength=620).pack(pady=40)

        tk.Button(self.quiz_container, text="RE-INITIALIZE EVALUATION", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  relief="flat", bd=1, width=30,
                  command=self.start_quiz).pack(pady=10)
        
        # Repack the quiz controls frame and update the start button text after quiz
        self.quiz_controls_frame.pack(pady=(30, 0), padx=20, fill="x")
        self.start_quiz_button.config(text=f"INITIATE BEHAVIORAL EVALUATION ({len(self.quiz_questions)} CYCLES)")

        self.status_var.set(f"EVALUATION RESULT: {self.quiz_score}/{total_questions_in_quiz}")
    
    def show_pda_results(self):
        # PDA quiz always has 20 questions
        total_pda_questions = len(self.current_pda_questions)
        pda_score_percent = (self.pda_score / total_pda_questions) * 100

        pda_msg = f"PDA EVALUATION COMPLETE\n\nSCORE: {self.pda_score}/{total_pda_questions}  ({pda_score_percent:.1f}%)\n\n"
        
        recommendation = ""
        if pda_score_percent >= 80: # Higher threshold for PDA to indicate strong readiness
            recommendation = "RECOMMENDATION: You exhibit strong indicators of relationship readiness. Your self-awareness and emotional regulation are commendable."
        elif pda_score_percent >= 60:
            recommendation = "RECOMMENDATION: You show potential for a healthy relationship, but some areas for self-reflection and growth are present. Consider working on emotional resilience."
        else:
            recommendation = "RECOMMENDATION: Significant self-reflection and growth are recommended before pursuing a serious relationship. Focus on understanding your patterns and needs."

        pda_msg += recommendation

        for widget in self.pda_container.winfo_children():
            widget.destroy()

        tk.Label(self.pda_container, text=pda_msg, font=("Consolas", 14, "bold"),
                 fg=COLOR_ACCENT, bg=COLOR_PANEL, wraplength=620).pack(pady=40)

        tk.Button(self.pda_container, text="RE-INITIALIZE PDA EVALUATION", font=FONT_BUTTON,
                  bg=COLOR_BUTTON_BG, fg=COLOR_ACCENT, activebackground=COLOR_BUTTON_HL,
                  relief="flat", bd=1, width=30,
                  command=self.start_pda_quiz).pack(pady=10)
        
        self.pda_controls_frame.pack(pady=(30, 0), padx=20, fill="x")
        self.start_pda_quiz_button.config(text=f"INITIATE PDA EVALUATION (20 CYCLES)") # Ensure text is correct

        self.status_var.set(f"PDA RESULT: {self.pda_score}/{total_pda_questions}")

# ────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AttentionApp(root)
    root.mainloop()