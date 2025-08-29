import tkinter as tk
from tkinter import messagebox  # Import messagebox explicitly
import random
import os

# Initialize the main window
root = tk.Tk()
root.title("Puzzle Game")
root.geometry("500x500")


# Global variables
grid = []
buttons = []
size = 4  # Default grid size
move_count = 0  # Initialize move counter
undo_stack = []  # Stack to store previous states for undo functionality
redo_stack = []  # Stack to store undone states for redo functionality
high_scores = {"Easy": float('inf'), "Medium": float('inf'), "Hard": float('inf')}  # High score tracker
difficulty = "Medium"  # Default difficulty

# Function to load high scores from file
def load_high_scores():
    global high_scores
    if os.path.exists("high_scores.txt"):
        try:
            with open("high_scores.txt", "r") as file:
                for line in file:
                    level, score = line.strip().split(":")
                    high_scores[level] = int(score)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            high_scores = {"Easy": float('inf'), "Medium": float('inf'), "Hard": float('inf')}

# Function to save high scores to file
def save_high_scores():
    try:
        with open("high_scores.txt", "w") as file:
            for level, score in high_scores.items():
                file.write(f"{level}:{score}\n")
    except Exception as e:
        print(f"Error saving high scores: {e}")

# Function to shuffle the grid
def shuffle_grid():
    global grid, move_count, undo_stack, redo_stack
    flattened = sum(grid, [])
    random.shuffle(flattened)
    grid = [flattened[i:i + size] for i in range(0, size * size, size)]
    move_count = 0  # Reset move counter after shuffle
    undo_stack = []  # Clear undo stack after shuffle
    redo_stack = []  # Clear redo stack after shuffle
    update_buttons()

# Function to update the buttons and move counter
def update_buttons():
    for i in range(size):
        for j in range(size):
            buttons[i][j]["text"] = grid[i][j]
    move_count_label.config(text=f"Moves: {move_count}")

# Function to check if the puzzle is solved
def is_solved():
    target = list(range(1, size * size)) + [""]
    flattened = sum(grid, [])
    return flattened == target

# Function to move a tile
def move_tile(row, col):
    global grid, move_count, undo_stack, redo_stack, high_scores, difficulty
    empty_row, empty_col = [(r, c) for r in range(size) for c in range(size) if grid[r][c] == ""][0]
    if abs(row - empty_row) + abs(col - empty_col) == 1:
        undo_stack.append([row[:] for row in grid])
        redo_stack.clear()  # Clear redo stack after a new move
        grid[empty_row][empty_col], grid[row][col] = grid[row][col], grid[empty_row][empty_col]
        move_count += 1
        update_buttons()
        if is_solved():
            if move_count < high_scores[difficulty]:
                high_scores[difficulty] = move_count
                save_high_scores()
            messagebox.showinfo(
                "Congratulations!",
                f"You solved the puzzle in {move_count} moves!\n"
                f"High Score for {difficulty}: {high_scores[difficulty]} moves."
            )

# Function to undo the last move
def undo_move():
    global grid, move_count, undo_stack, redo_stack
    if undo_stack:
        redo_stack.append([row[:] for row in grid])
        grid = undo_stack.pop()
        move_count -= 1
        update_buttons()
    else:
        messagebox.showinfo("Undo", "No more moves to undo!")

# Function to redo the last undone move
def redo_move():
    global grid, move_count, redo_stack
    if redo_stack:
        undo_stack.append([row[:] for row in grid])
        grid = redo_stack.pop()
        move_count += 1
        update_buttons()
    else:
        messagebox.showinfo("Redo", "No more moves to redo!")

# Function to start the game with a selected level
def start_game(level):
    global size, grid, buttons, move_count_label, undo_stack, redo_stack, difficulty
    difficulty = level
    size = {"Easy": 3, "Medium": 4, "Hard": 5}[level]
    grid = [[(i * size + j + 1) for j in range(size)] for i in range(size)]
    grid[-1][-1] = ""  # Empty tile
    buttons = [[None for _ in range(size)] for _ in range(size)]
    for widget in root.winfo_children():
        widget.destroy()  # Clear the screen
    for i in range(size):
        for j in range(size):
            btn = tk.Button(root, text=grid[i][j], font=("Arial", 20), width=5, height=2,
                            command=lambda row=i, col=j: move_tile(row, col))
            btn.grid(row=i, column=j, padx=5, pady=5)
            buttons[i][j] = btn
    move_count = 0
    undo_stack = []
    redo_stack = []
    move_count_label = tk.Label(root, text=f"Moves: {move_count}", font=("Arial", 16))
    move_count_label.grid(row=size, column=0, columnspan=size)
    shuffle_button = tk.Button(root, text="Shuffle", font=("Arial", 14), command=shuffle_grid)
    shuffle_button.grid(row=size + 1, column=0, columnspan=size // 3, pady=10)
    undo_button = tk.Button(root, text="Undo", font=("Arial", 14), command=undo_move)
    undo_button.grid(row=size + 1, column=size // 3, columnspan=size // 3, pady=10)
    redo_button = tk.Button(root, text="Redo", font=("Arial", 14), command=redo_move)
    redo_button.grid(row=size + 1, column=2 * size // 3, columnspan=size // 3, pady=10)

# Function to show the level selection menu
def level_menu():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Choose Difficulty Level", font=("Arial", 20)).pack(pady=20)
    tk.Button(root, text="Easy (3x3)", font=("Arial", 16), command=lambda: start_game("Easy")).pack(pady=10)
    tk.Button(root, text="Medium (4x4)", font=("Arial", 16), command=lambda: start_game("Medium")).pack(pady=10)
    tk.Button(root, text="Hard (5x5)", font=("Arial", 16), command=lambda: start_game("Hard")).pack(pady=10)

load_high_scores()
level_menu()
root.mainloop()
