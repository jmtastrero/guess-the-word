import tkinter as tk
from tkinter import messagebox, ttk
import random

WORDS = [
    {"word": "python", "hint": "A popular programming language 🐍", "fake": "A snake that can fly"},
    {"word": "galaxy", "hint": "A massive collection of stars 🌌", "fake": "A brand of coffee"},
    {"word": "ocean", "hint": "Covers 70% of the Earth 🌊", "fake": "A type of hot desert"},
    {"word": "gravity", "hint": "Keeps you from floating away 🌍", "fake": "A famous dance move"},
    {"word": "volcano", "hint": "A mountain that erupts lava 🌋", "fake": "A frozen ice mountain"},
    {"word": "nebula", "hint": "A cloud of space dust and gas", "fake": "A small tropical fruit"},
    {"word": "quantum", "hint": "A field of physics dealing with tiny particles", "fake": "A type of kitchen knife"},
    {"word": "horizon", "hint": "Where the sky meets the Earth", "fake": "A brand of electric cars"},
    {"word": "algorithm", "hint": "Step-by-step instructions for solving a problem", "fake": "A type of musical instrument"},
    {"word": "oxygen", "hint": "Gas needed to breathe", "fake": "A new phone model"},
    {"word": "photosynthesis", "hint": "Plants converting light into energy", "fake": "A camera editing technique"},
    {"word": "asteroid", "hint": "A rocky object orbiting the Sun", "fake": "A type of video game console"},
    {"word": "bacteria", "hint": "Tiny living organisms", "fake": "A kind of Italian sauce"},
    {"word": "fusion", "hint": "Combining atoms to release energy", "fake": "A hairstyle trend"},
    {"word": "hologram", "hint": "A 3D projected image", "fake": "A type of food seasoning"},
    {"word": "ecosystem", "hint": "A community of living things", "fake": "A gaming platform"},
    {"word": "tsunami", "hint": "A huge wave caused by earthquakes", "fake": "A type of sushi"},
    {"word": "meteor", "hint": "A space rock entering the atmosphere", "fake": "A rare type of potato"},
    {"word": "enzyme", "hint": "A protein that speeds up chemical reactions", "fake": "A wristwatch brand"},
    {"word": "plasma", "hint": "A hot, ionized state of matter", "fake": "A famous painting style"},
    {"word": "orbit", "hint": "The path of something around a planet", "fake": "A new social media app"},
    {"word": "avalanche", "hint": "A mass of snow rushing downhill", "fake": "A sports drink flavor"},
    {"word": "species", "hint": "A group of similar organisms", "fake": "A luxury car brand"},
    {"word": "hydrate", "hint": "Give the body water", "fake": "A computer term"},
    {"word": "equator", "hint": "Line dividing Earth in half", "fake": "A cooking utensil"},
    {"word": "friction", "hint": "Force resisting motion", "fake": "A soft type of fabric"},
    {"word": "momentum", "hint": "Mass in motion", "fake": "A hotel chain"},
    {"word": "hemisphere", "hint": "Half of Earth", "fake": "A hairstyle"},
    {"word": "turbine", "hint": "Machine extracting energy", "fake": "A type of bread"},
    {"word": "avocado", "hint": "Green fruit w/ big seed", "fake": "A martial art"},
]

MAX_LIVES = 10
TIME_LIMIT = 60


class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess The Word - Premium Edition")
        self.root.geometry("700x650")
        self.root.config(bg="#1e1e2f")
        self.root.resizable(False, False)

        self.word = ""
        self.display = []
        self.used_letters = []
        self.lives = MAX_LIVES
        self.time_left = TIME_LIMIT
        self.running = True

        self.create_ui()
        self.start_game()
        self.update_timer()

    # -------------------------------------------------------------
    #                          UI SETUP
    # -------------------------------------------------------------
    def create_ui(self):
        self.title_lbl = tk.Label(
            self.root, text="🌀 Guess the Word",
            font=("Segoe UI", 20, "bold"), fg="white", bg="#1e1e2f"
        )
        self.title_lbl.pack(pady=8)

        self.hint_lbl = tk.Label(
            self.root, text="", font=("Segoe UI", 14),
            fg="#f8e7a1", bg="#1e1e2f", wraplength=600
        )
        self.hint_lbl.pack(pady=5)

        self.word_lbl = tk.Label(
            self.root, text="", font=("Consolas", 30, "bold"),
            fg="white", bg="#1e1e2f"
        )
        self.word_lbl.pack(pady=8)

        self.info_lbl = tk.Label(
            self.root, text="", font=("Segoe UI", 12),
            fg="#bbbbbb", bg="#1e1e2f"
        )
        self.info_lbl.pack(pady=4)

        self.timer_bar = ttk.Progressbar(self.root, length=400, maximum=TIME_LIMIT)
        self.timer_bar.pack(pady=5)

        # ----------------------------
        #     KEYBOARD (QWERTY)
        # ----------------------------
        self.kb_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.kb_frame.pack(pady=10)

        layout = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        self.keyboard_buttons = {}

        for r, row_letters in enumerate(layout):
            row_frame = tk.Frame(self.kb_frame, bg="#1e1e2f")
            row_frame.pack()

            for ch in row_letters:
                btn = tk.Button(
                    row_frame, text=ch, width=4, height=2,
                    font=("Segoe UI", 12, "bold"),
                    bg="#3b3b55", fg="white", relief="flat",
                    command=lambda l=ch.lower(): self.guess_letter(l)
                )
                btn.pack(side="left", padx=4, pady=4)
                self.keyboard_buttons[ch.lower()] = btn

        # Restart button
        self.restart_btn = tk.Button(
            self.root, text="Restart Game",
            font=("Segoe UI", 12), bg="#4b8cf5",
            fg="white", width=15, command=self.start_game
        )
        self.restart_btn.pack(pady=10)

    # -------------------------------------------------------------
    def start_game(self):
        entry = random.choice(WORDS)
        self.word = entry["word"]
        self.display = ["_"] * len(self.word)
        self.used_letters = []
        self.lives = MAX_LIVES
        self.time_left = TIME_LIMIT
        self.running = True

        hint = entry["hint"] if random.choice([True, False]) else entry["fake"]
        self.real_hint = (hint == entry["hint"])
        self.hint_lbl.config(text="💡 " + hint)

        for btn in self.keyboard_buttons.values():
            btn.config(state="normal", bg="#3b3b55")

        self.refresh_display()

    def refresh_display(self):
        self.word_lbl.config(text=" ".join(self.display))
        self.info_lbl.config(
            text=f"❤️ Lives: {self.lives} | 🔠 Used: {', '.join(self.used_letters).upper() or 'None'}"
        )

    # -------------------------------------------------------------
    def guess_letter(self, letter):
        if not self.running:
            return

        self.used_letters.append(letter)
        self.keyboard_buttons[letter].config(state="disabled", bg="#222237")

        if letter in self.word:
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.display[i] = letter
        else:
            self.lives -= 1

        self.refresh_display()
        self.check_endgame()

    # -------------------------------------------------------------
    def show_game_over_buttons(self):
        self.over_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.over_frame.pack(pady=10)

        tk.Button(
            self.over_frame, text="Try Again",
            font=("Segoe UI", 12), width=12,
            bg="#28a745", fg="white",
            command=lambda: [self.over_frame.destroy(), self.start_game()]
        ).pack(side="left", padx=10)

        tk.Button(
            self.over_frame, text="Quit",
            font=("Segoe UI", 12), width=12,
            bg="#d9534f", fg="white",
            command=self.root.destroy
        ).pack(side="left", padx=10)

    # -------------------------------------------------------------
    def check_endgame(self):
        if "_" not in self.display:
            self.running = False
            messagebox.showinfo("Victory!", "🎉 You guessed the word!")
            return

        if self.lives <= 0:
            self.running = False
            messagebox.showerror("Game Over", f"The word was: {self.word.upper()}")
            self.show_game_over_buttons()

    # -------------------------------------------------------------
    def update_timer(self):
        if self.running:
            self.time_left -= 1
            self.timer_bar["value"] = TIME_LIMIT - self.time_left

            if self.time_left <= 0:
                self.running = False
                messagebox.showerror("Time's Up!", f"The word was: {self.word.upper()}")
                self.show_game_over_buttons()

        self.root.after(1000, self.update_timer)


root = tk.Tk()
game = WordGame(root)
root.mainloop()