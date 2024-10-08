import tkinter as tk
import random
from copy import deepcopy

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.window.geometry("400x620")
        self.board = [[0] * 4 for _ in range(4)]
        self.prev_boards = []  # To store previous board states for undo
        self.undo_count = 0  # Track the number of undos performed
        self.max_undo_count = 3  # Set the maximum number of undos allowed
        self.score = 0
        self.difficulty = 'Easy'  # Default difficulty
        self.highest_score = self.load_highest_score()
        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=5)

        self.highest_score_label = tk.Label(self.window, text=f"Highest Score: {self.highest_score}", font=("Helvetica", 14))
        self.highest_score_label.pack(pady=5)

        self.highest_sum_label = tk.Label(self.window, text="Highest Sum: 0", font=("Helvetica", 14))
        self.highest_sum_label.pack(pady=5)

        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="#CDC1B4")
        self.canvas.pack()

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)

        self.restart_button = tk.Button(button_frame, text="Restart", command=self.new_game)
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(button_frame, text="Undo", command=self.undo_move)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(button_frame, text="Quit", command=self.window.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_command(label="Save Game", command=self.save_game)
        file_menu.add_command(label="Load Game", command=self.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Settings", command=self.show_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Play", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.window.bind("<Key>", self.key_pressed)

    def new_game(self):
        self.score = 0
        self.board = [[0] * 4 for _ in range(4)]
        self.prev_boards = []
        for _ in range(2):
            self.add_new_tile()
        self.update_board()
        self.undo_count = 0
        self.update_undo_button_state()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4

    def update_board(self):
        self.canvas.delete("tile")
        color_mapping = {
            0: "#CDC1B4",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E",
        }
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                color = color_mapping.get(value, "#CDC1B4")
                self.canvas.create_rectangle(j * 100, i * 100, (j + 1) * 100, (i + 1) * 100, fill=color, tags="tile")
                if value != 0:
                    self.canvas.create_text((j + 0.5) * 100, (i + 0.5) * 100, text=str(value), font=("Helvetica", 36, "bold"), tags="tile")

        self.score_label.config(text=f"Score: {self.score}")
        self.highest_score_label.config(text=f"Highest Score: {self.highest_score}")
        self.update_highest_sum()
        self.canvas.update()

    def update_highest_sum(self):
        highest_sum = max(map(max, self.board))
        self.highest_sum_label.config(text=f"Highest Sum: {highest_sum}")

    def key_pressed(self, event):
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right']:
            self.prev_boards.append(deepcopy(self.board))
            self.move_tiles(key)
            self.add_new_tile()
            self.update_board()
            if self.is_game_over():
                self.game_over()
                self.update_highest_score()

    def move_tiles(self, direction):
        if self.difficulty=="Easy":
            if direction in ['Left', 'Right']:
                for i in range(4):
                    if direction == 'Left':
                        self.board[i] = self.move_row(self.board[i])
                    else:  # direction == 'Right'
                        self.board[i] = self.move_row(self.board[i][::-1])[::-1]
            elif direction in ['Up', 'Down']:
                for j in range(4):
                    column = [self.board[i][j] for i in range(4)]
                    if direction == 'Up':
                        new_column = self.move_row(column)
                    else:  # direction == 'Down'
                        new_column = self.move_row(column[::-1])[::-1]
                    for i in range(4):
                        self.board[i][j] = new_column[i]
        else:#difficult mode
            if direction == 'Up':
                self.board = [list(x) for x in zip(*self.board)]
                self.board = [self.move_row(row) for row in self.board]
                self.board = [list(x[::-1]) for x in zip(*self.board)]
            elif direction == 'Down':
                self.board = [list(x) for x in zip(*self.board[::-1])]
                self.board = [self.move_row(row) for row in self.board]
                self.board = [list(x[::-1]) for x in zip(*self.board)]
            elif direction == 'Left':
                self.board = [self.move_row(row) for row in self.board]
            elif direction == 'Right':
                self.board = [row[::-1] for row in self.board]
                self.board = [self.move_row(row) for row in self.board]
                self.board = [list(x[::-1]) for x in zip(*self.board)]
    def move_row(self, row):
        new_row = [tile for tile in row if tile != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row.pop(i + 1)
                new_row.append(0)
        return new_row + [0] * (4 - len(new_row))

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

    def game_over(self):
        self.canvas.create_text(200, 200, text="YOU LOSE", font=("Helvetica", 36, "bold"), fill="red")
        self.canvas.update()

    def update_highest_score(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            self.save_highest_score()

    def save_highest_score(self):
        try:
            with open("highest_score.txt", "w") as file:
                file.write(str(self.highest_score))
        except IOError as e:
            print(f"Error saving high score: {e}")

    def load_highest_score(self):
        try:
            with open("highest_score.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading high score: {e}")
            return 0

    def undo_move(self):
        if len(self.prev_boards) > 0 and self.undo_count < self.max_undo_count:
            self.board = self.prev_boards.pop()
            self.update_board()
            self.undo_count += 1
            self.update_undo_button_state()

    def update_undo_button_state(self):
        if self.undo_count == self.max_undo_count:
            self.undo_button.config(state=tk.DISABLED)
        else:
            self.undo_button.config(state=tk.NORMAL)

    def save_game(self):
        try:
            with open("saved_game.txt", "w") as file:
                for row in self.board:
                    file.write(" ".join(map(str, row)) + "\n")
                file.write(f"Score: {self.score}\n")
        except IOError as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        try:
            with open("saved_game.txt", "r") as file:
                lines = file.readlines()
                self.board = [list(map(int, line.strip().split())) for line in lines[:4]]
                self.score = int(lines[4].split(": ")[1])
                self.update_board()
        except IOError as e:
            print(f"Error loading game: {e}")

    def show_settings(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Settings")
        settings_window.geometry("300x150")
        
        difficulty_label = tk.Label(settings_window, text="Difficulty Level:")
        difficulty_label.pack(pady=10)
        
        easy_button = tk.Button(settings_window, text="Easy", command=lambda: self.set_difficulty('Easy'))
        easy_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        difficult_button = tk.Button(settings_window, text="Difficult", command=lambda: self.set_difficulty('Difficult'))
        difficult_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def set_difficulty(self, level):
        self.difficulty = level
        print(f"Difficulty set to: {self.difficulty}")
        # Implement the logic to adjust game difficulty if needed

    def show_about(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("How to Play")
        help_text = """ TEAM 2 PROJECT WORK """   
        help_label = tk.Label(help_window, text=help_text, font=("Helvetica", 12))
        help_label.pack(padx=10, pady=10, fill="both", expand=True)    

    def show_help(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("How to Play")
        help_text = """
        Welcome to 2048!

        Objective:
        The objective of the game is to slide numbered tiles on a grid to combine them to create a tile with the number 2048.

        How to Play:
        - Use the arrow keys to move the tiles in different directions: Up, Down, Left, or Right.
        - Tiles with the same number will merge into one when they collide.
        - After each move, a new tile will randomly appear in an empty spot with a value of either 2 or 4.
        - Continue merging tiles to reach the 2048 tile and win the game!
        - The game ends when the grid is full and no more moves can be made.

        Tips:
        - Plan your moves carefully to avoid filling up the grid too quickly.
        - Try to keep your high-value tiles in one corner to maximize space for new tiles.
        - Don't be afraid to use the Undo button if you make a mistake!

        Have fun and enjoy playing 2048!
        """
        help_label = tk.Label(help_window, text=help_text, font=("Helvetica", 12))
        help_label.pack(padx=10, pady=10, fill="both", expand=True)


    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.run()
