# Full-Featured Python Chess Game (Tkinter + AI)

This project is a full chess application I built using Python and Tkinter.  
It includes all the standard chess mechanics, a simple AI opponent with difficulty levels, save/load features, and checkmate/stalemate detection.  
Everything runs locally with no external dependencies besides Python’s standard library.

---

# Folder Structure

## chess_project

### game
- _init_.py
- utilities.py
- state.py
- ai.py

### ui
- _init_.py
- gui.py

### main.py


# What each file does


### main.py
This is the main entry point for the game.  
It just creates the Tkinter window and launches the GUI.

To run the file open the terminal on your IDE(either VS code, Pycharm or whichever one you use and type)

```python
import tkinter as tk
from ui.gui import ChessGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()

```

---

### ui/gui.py

This is where I built the full Tkinter user interface.
It handles:

- Drawing the chessboard and pieces

- Handling user clicks for moves

- Displaying move history

- Saving and loading games

- Updating the board after each move

- Triggering the AI opponent when enabled


We used a Canvas widget for the board and a side Listbox to display move history.
Buttons for Undo, Restart, Save, and Load are also included.

Important Methods:

- `draw_board()`: Draws the 8x8 chess grid and pieces.

- `on_click()`: Handles user selection and moves.

- `check_post_move()`: Checks for checkmate, stalemate, and draws.

- `schedule_ai_move()` and `make_ai_move()`: Runs AI turns automatically after the player moves.

- `save_game()` / `load_game()`: Uses JSON for saving and restoring game state.


---

### game/state.py

This file manages the actual chess logic — the current position, turns, move legality, and history.
I keep everything in a GameState class.

Key Responsibilities:

- Keeping track of the board (an 8x8 list)

- Determining whose turn it is

- Generating legal moves for each side

- Detecting checks, checkmate, and stalemate

- Enforcing en-passant, castling, and pawn promotion

- Storing move history for undo and save/load

Notable Methods:

- `generate_legal_moves(side)`: Returns a list of all legal moves for the given color.

- `make_move(r, c, nr, nc)`: Moves a piece and updates game state.

- `is_in_check(side)`: Detects if a side’s king is under attack.

- `undo()`: Reverses the last move.

- `save_json()` / `load_json()`: Serializes and deserializes the entire game into JSON format.

---

### game/utilities.py

This file defines the behavior of each chess piece type.
Every piece (King, Queen, Rook, Bishop, Knight, Pawn) is a subclass of a base Piece class.

Example:

1. The King class includes castling logic.

2. The Pawn class handles en-passant and promotion.

3. The Rook and Bishop generate sliding moves.

4. The Knight uses fixed offsets.

Each piece class has a method like:

```python
def get_moves(self, board, r, c):
    # returns list of (new_row, new_col) for legal moves
```

### game/ai.py

This file handles the computer opponent.

I added three difficulty levels:

1. Easy: Random legal move

2. Medium: Random legal move but tries to capture if possible

3. Hard: Basic logic that prioritizes material advantage

The AI uses the same move generation logic as the human player.
It doesn’t use deep chess heuristics but it’s fun and fast.

Key Function:
```python
def ai_choose_move(state, level, side):
    # returns (r, c, nr, nc)
```

### Implemented Features
- ✅ Click-to-move GUI
- ✅	En-passant
- ✅	Castling
- ✅	Pawn Promotion
- ✅	Check / Checkmate / Stalemate detection
- ✅	Undo Move
- ✅	Save / Load (JSON format)
- ✅	AI Opponent (Easy / Medium / Hard)
- ✅	Move History
- ✅	Restart Game
- ✅	GUI-based Alerts for Game Over

---

# How to Run the Game

1. Make sure you have Python 3 installed.

2. Navigate to the project folder.

3. Run the main file:
```python
python main.py
```
The Tkinter window will open automatically.

---

# How the Game Works Internally

Whenever you click a piece:

The on_click() method checks if it’s your turn.

If valid, it highlights possible moves.

Clicking a valid square makes the move.

The game state updates, move history records, and AI moves (if enabled).

If the AI is playing, it automatically makes a move after a short delay using schedule_ai_move().

Each move triggers check_post_move() to verify if the game has ended in checkmate or stalemate.

Saving and Loading Games

When you click Save, the current game state is stored as a .json file.
Load restores everything (board position, move history, turn, etc.) exactly as it was.

---

# 🤖AI Overview

The AI’s logic is based on move generation and a simple scoring system:

Pawns = 1

Knights / Bishops = 3

Rooks = 5

Queens = 9

In hard mode, it looks one move ahead and tries to choose moves that maximize material value.

---


# 🗒️Notes

GUI runs entirely on Tkinter (no Pygame needed)

Saves are in plain JSON for easy debugging

The AI intentionally plays imperfectly to keep it fun

You can easily modify piece images or colors in `draw_board()`

# 🧑‍💻Authors 
Group 20
1. Akwada Emmanuel Chinedu (Group Leader)
2. Abdullahi Saleh Abdullahi
3. Ahmad Alhaji Ali