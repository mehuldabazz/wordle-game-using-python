import tkinter as tk
from tkinter import messagebox
import random

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")

        self.words = [
            "snail", "crane", "flint", "blitz", "cable", "dwarf", "pride", "flame", "jolly", "wound",
            "tiger", "quest", "vivid", "whale", "bloom", "grace", "mirth", "spice", "piano", "storm",
            "lucky", "binge", "crisp", "grove", "joint", "kneel", "lemon", "mango", "noble", "ocean",
            "pearl", "quiet", "raven", "shard", "tribe", "uncle", "viper", "woven", "xerox", "yacht",
            "zebra", "alpha", "brave", "chant", "delve", "evoke", "forge", "gloat", "hasty", "index"
        ]

        self.hidden_word = random.choice(self.words)
        self.attempts = 6
        self.current_attempt = 0

        self.create_widgets()

    def create_widgets(self):
        # Instructions Label
        self.instructions = tk.Label(self.root, text="Guess the five-letter word!", font=("Helvetica", 14))
        self.instructions.pack(pady=10)

        # Attempts Label
        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts}", font=("Helvetica", 12))
        self.attempts_label.pack(pady=5)

        # Frame for guess entries
        self.entries_frame = tk.Frame(self.root)
        self.entries_frame.pack(pady=10)

        # Create a grid of entry widgets
        self.entries = []
        for i in range(self.attempts):
            entry_row = []
            for j in range(5):
                entry = tk.Entry(self.entries_frame, width=4, font=("Helvetica", 24), justify='center', state='disabled')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.bind('<KeyRelease>', self.next_cell)
                entry_row.append(entry)
            self.entries.append(entry_row)

        # Enable the first row for input
        for entry in self.entries[0]:
            entry.config(state='normal')

        # Bind the Return key to check the guess
        self.root.bind('<Return>', self.check_guess)

    def next_cell(self, event):
        row = self.current_attempt
        col = int(event.widget.grid_info()['column'])

        # Move to the next cell if a letter is typed
        if col < 4 and event.keysym.isalpha() and len(event.widget.get()) == 1:
            self.entries[row][col + 1].config(state='normal')
            self.entries[row][col + 1].focus_set()
        # Clear the cell if backspace is pressed
        elif event.keysym == 'BackSpace' and col > 0:
            self.entries[row][col - 1].config(state='normal')
            self.entries[row][col - 1].focus_set()
            self.entries[row][col - 1].delete(0, tk.END)

    def check_guess(self, event):
        guess = "".join([self.entries[self.current_attempt][i].get() for i in range(5)]).lower()

        if len(guess) != 5:
            messagebox.showerror("Error", "Please enter a five-letter word.")
            return

        feedback = self.evaluate_guess(guess)

        for i, entry in enumerate(self.entries[self.current_attempt]):
            entry.config(state='disabled', disabledbackground=feedback[i][1], disabledforeground='white')

        if guess == self.hidden_word:
            messagebox.showinfo("Congratulations!", "You guessed the word correctly! WIN 🕺🕺🕺")
            self.root.quit()
            return

        self.current_attempt += 1
        self.attempts -= 1
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")

        if self.current_attempt < 6:
            for i in range(5):
                self.entries[self.current_attempt][i].config(state='normal')
            self.entries[self.current_attempt][0].focus_set()
        else:
            messagebox.showinfo("Game Over", f"Game over! The hidden word was '{self.hidden_word}'.")
            self.root.quit()

    def evaluate_guess(self, guess):
        feedback = []
        for i, char in enumerate(guess):
            if char == self.hidden_word[i]:
                feedback.append((char, 'green'))
            elif char in self.hidden_word:
                feedback.append((char, 'yellow'))
            else:
                feedback.append((char, 'gray'))
        return feedback

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()
