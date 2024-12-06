import tkinter as tk
from tkinter import messagebox
import random

class Game2048:
    def __init__(self, master):  # Fixed constructor name
        self.master = master
        self.master.title("2048 Game")
        self.grid_size = 4
        self.tiles = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.previous_state = None

        self.colors = {
            0: "lightgrey", 2: "lightyellow", 4: "lightgoldenrod",
            8: "orange", 16: "darkorange", 32: "tomato",
            64: "red", 128: "yellowgreen", 256: "green",
            512: "blue", 1024: "purple", 2048: "gold"
        }

        self.board_frame = tk.Frame(self.master, bg="grey", bd=3)
        self.board_frame.grid()
        self.create_grid()
        self.spawn_tile()
        self.spawn_tile()
        self.update_grid()

        # Bind movement keys
        self.master.bind("<Up>", lambda event: self.move("Up"))
        self.master.bind("<Down>", lambda event: self.move("Down"))
        self.master.bind("<Left>", lambda event: self.move("Left"))
        self.master.bind("<Right>", lambda event: self.move("Right"))
        self.master.bind("<u>", lambda event: self.undo())  # Added undo functionality binding

    def create_grid(self):
        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell = tk.Label(self.board_frame, text="", bg=self.colors[0], font=("Helvetica", 24), width=4, height=2)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

    def spawn_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.tiles[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.tiles[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.tiles[i][j]
                self.cells[i][j].config(text=str(value) if value else "", bg=self.colors[value])

    def move(self, direction):
        self.save_state()
        if direction in ("Up", "Down"):
            self.tiles = list(map(list, zip(*self.tiles)))  # Transpose for vertical moves
        moved = self.slide_and_merge()
        if direction in ("Up", "Down"):
            self.tiles = list(map(list, zip(*self.tiles)))  # Re-transpose
        if moved:
            self.spawn_tile()
            self.update_grid()
            if self.check_game_over():
                self.end_game()

    def slide_and_merge(self):
        moved = False
        for row in self.tiles:
            compressed = [num for num in row if num != 0]
            for i in range(len(compressed) - 1):
                if compressed[i] == compressed[i + 1]:
                    compressed[i] *= 2
                    compressed[i + 1] = 0
                    self.score += compressed[i]
            merged = [num for num in compressed if num != 0]
            merged += [0] * (self.grid_size - len(merged))
            if row != merged:
                moved = True
            row[:] = merged
        return moved

    def save_state(self):
        self.previous_state = [row[:] for row in self.tiles]

    def undo(self):
        if self.previous_state:
            self.tiles = [row[:] for row in self.previous_state]
            self.update_grid()

    def check_game_over(self):
        if any(0 in row for row in self.tiles):
            return False
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (j + 1 < self.grid_size and self.tiles[i][j] == self.tiles[i][j + 1]) or \
                   (i + 1 < self.grid_size and self.tiles[i][j] == self.tiles[i + 1][j]):
                    return False
        return True

    def end_game(self):
        messagebox.showinfo("Game Over", f"Your score: {self.score}")
        self.master.destroy()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
