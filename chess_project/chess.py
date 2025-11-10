import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from copy import deepcopy
import random
import json
import math

PIECE_UNICODE = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
}

FILES = 'abcdefgh'

class GameState:
    def __init__(self):
        self.board = self.create_starting_board()
        self.white_to_move = True
        # castling rights: [white_kingside, white_queenside, black_kingside, black_queenside]
        self.castling = [True, True, True, True]
        # en-passant target square as (r,c) where a pawn may be captured, or None
        self.en_passant = None
        self.move_history = []
        self.halfmove_clock = 0
        self.fullmove_number = 1

    def create_starting_board(self):
        # NOTE: this board orientation places White back rank on row 0 (top of array),
        # and White pawns on row 1. GUI inverts rows visually.
        b = [[None for _ in range(8)] for _ in range(8)]
        # Pawns
        for c in range(8):
            b[1][c] = 'P'  # white pawns
            b[6][c] = 'p'  # black pawns
        # White back rank (row 0)
        b[0][0] = b[0][7] = 'R'
        b[0][1] = b[0][6] = 'N'
        b[0][2] = b[0][5] = 'B'
        b[0][3] = 'Q'
        b[0][4] = 'K'
        # Black back rank (row 7)
        b[7][0] = b[7][7] = 'r'
        b[7][1] = b[7][6] = 'n'
        b[7][2] = b[7][5] = 'b'
        b[7][3] = 'q'
        b[7][4] = 'k'
        return b

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def is_white(self, piece):
        return piece is not None and piece.isupper()

    def is_black(self, piece):
        return piece is not None and piece.islower()

    def ally(self, piece):
        if piece is None: return None
        return 'white' if self.is_white(piece) else 'black'

    def locate_king(self, color, board=None):
        target = 'K' if color == 'white' else 'k'
        board = board if board is not None else self.board
        for r in range(8):
            for c in range(8):
                if board[r][c] == target:
                    return (r,c)
        return None

    def piece_attacks_square(self, src, dst, board):
        r,c = src
        tr, tc = dst
        p = board[r][c]
        if p is None: return False
        color = 'white' if p.isupper() else 'black'
        pl = p.lower()
        dr = tr - r
        dc = tc - c

        if pl == 'p':
            # pawns attack one forward-diagonal relative to their color
            direction = 1 if color == 'white' else -1
            return dr == direction and abs(dc) == 1
        if pl == 'n':
            return (abs(dr), abs(dc)) in [(1,2),(2,1)]
        if pl == 'b':
            if abs(dr) != abs(dc) or dr == 0: return False
            step_r = 1 if dr>0 else -1
            step_c = 1 if dc>0 else -1
            rr, cc = r+step_r, c+step_c
            while (rr,cc) != (tr,tc):
                if board[rr][cc] is not None: return False
                rr += step_r; cc += step_c
            return True
        if pl == 'r':
            if dr != 0 and dc != 0: return False
            step_r = 0 if dr==0 else (1 if dr>0 else -1)
            step_c = 0 if dc==0 else (1 if dc>0 else -1)
            rr, cc = r+step_r, c+step_c
            while (rr,cc) != (tr,tc):
                if board[rr][cc] is not None: return False
                rr += step_r; cc += step_c
            return True
        if pl == 'q':
            if (abs(dr) == abs(dc) and dr != 0) or (dr == 0 and dc != 0) or (dc == 0 and dr != 0):
                step_r = 0 if dr==0 else (1 if dr>0 else -1)
                step_c = 0 if dc==0 else (1 if dc>0 else -1)
                rr, cc = r+step_r, c+step_c
                while (rr,cc) != (tr,tc):
                    if board[rr][cc] is not None: return False
                    rr += step_r; cc += step_c
                return True
            return False
        if pl == 'k':
            return max(abs(dr), abs(dc)) == 1
        return False

    def is_in_check(self, color, board=None):
        board = board if board is not None else self.board
        king_pos = self.locate_king(color, board)
        if not king_pos:
            # no king found -> treat as check
            return True
        kr, kc = king_pos
        enemy = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p is None: continue
                if enemy == 'white' and not p.isupper(): continue
                if enemy == 'black' and not p.islower(): continue
                if self.piece_attacks_square((r,c),(kr,kc),board):
                    return True
        return False

    def generate_moves_for_square(self, r, c):
        piece = self.board[r][c]
        if piece is None: return []
        color = 'white' if piece.isupper() else 'black'
        direction = 1 if color == 'white' else -1
        moves = []
        p = piece.lower()
        if p == 'p':
            fr = r + direction
            if self.in_bounds(fr, c) and self.board[fr][c] is None:
                moves.append((fr, c))
                start_row = 1 if color == 'white' else 6
                fr2 = r + 2*direction
                if r == start_row and self.in_bounds(fr2, c) and self.board[fr2][c] is None:
                    moves.append((fr2, c))
            # captures
            for dc in (-1, 1):
                fc = c + dc
                if self.in_bounds(fr, fc):
                    target = self.board[fr][fc]
                    if target is not None and self.ally(target) != color:
                        moves.append((fr, fc))
            # en-passant
            if self.en_passant:
                ep_r, ep_c = self.en_passant
                if fr == ep_r and abs(ep_c - c) == 1:
                    moves.append((fr, ep_c))
        elif p == 'n':
            for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                nr, nc = r+dr, c+dc
                if not self.in_bounds(nr, nc): continue
                if self.board[nr][nc] is None or self.ally(self.board[nr][nc]) != color:
                    moves.append((nr, nc))
        elif p in ('b','r','q'):
            directions = []
            if p in ('b','q'):
                directions += [(1,1),(1,-1),(-1,1),(-1,-1)]
            if p in ('r','q'):
                directions += [(1,0),(-1,0),(0,1),(0,-1)]
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                while self.in_bounds(nr, nc):
                    if self.board[nr][nc] is None:
                        moves.append((nr, nc))
                    else:
                        if self.ally(self.board[nr][nc]) != color:
                            moves.append((nr, nc))
                        break
                    nr += dr; nc += dc
        elif p == 'k':
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr == 0 and dc == 0: continue
                    nr, nc = r+dr, c+dc
                    if not self.in_bounds(nr, nc): continue
                    if self.board[nr][nc] is None or self.ally(self.board[nr][nc]) != color:
                        moves.append((nr, nc))
            # castling checks
            if color == 'white' and r == 0 and c == 4:
                # kingside
                if self.castling[0] and self.board[0][5] is None and self.board[0][6] is None:
                    if not self.is_in_check('white') and not self.square_under_attack((0,5),'white') and not self.square_under_attack((0,6),'white'):
                        moves.append((0,6))
                # queenside
                if self.castling[1] and self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None:
                    if not self.is_in_check('white') and not self.square_under_attack((0,3),'white') and not self.square_under_attack((0,2),'white'):
                        moves.append((0,2))
            if color == 'black' and r == 7 and c == 4:
                if self.castling[2] and self.board[7][5] is None and self.board[7][6] is None:
                    if not self.is_in_check('black') and not self.square_under_attack((7,5),'black') and not self.square_under_attack((7,6),'black'):
                        moves.append((7,6))
                if self.castling[3] and self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None:
                    if not self.is_in_check('black') and not self.square_under_attack((7,3),'black') and not self.square_under_attack((7,2),'black'):
                        moves.append((7,2))
        return moves

    def square_under_attack(self, square, color):
        sr, sc = square
        enemy = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is None: continue
                if enemy == 'white' and not p.isupper(): continue
                if enemy == 'black' and not p.islower(): continue
                if self.piece_attacks_square((r,c),(sr,sc), self.board):
                    return True
        return False

    def generate_legal_moves(self, for_color=None):
        color = for_color if for_color is not None else ('white' if self.white_to_move else 'black')
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is None: continue
                if color == 'white' and not piece.isupper(): continue
                if color == 'black' and not piece.islower(): continue
                candidates = self.generate_moves_for_square(r,c)
                for nr,nc in candidates:
                    new_board = deepcopy(self.board)
                    moving = new_board[r][c]
                    # handle en-passant simulated capture:
                    if moving and moving.lower() == 'p' and self.en_passant and (nr, nc) == self.en_passant and new_board[nr][nc] is None:
                        capture_r = r
                        capture_c = nc
                        # captured pawn is on rank r (behind target square)
                        new_board[capture_r][capture_c] = None
                    new_board[nr][nc] = new_board[r][c]
                    new_board[r][c] = None
                    if not self.is_in_check(color, new_board):
                        moves.append((r,c,nr,nc))
        return moves

    def make_move(self, r, c, nr, nc, promotion_choice=None):
        piece = self.board[r][c]
        if piece is None: return False
        color = 'white' if piece.isupper() else 'black'
        legal = False
        for mv in self.generate_legal_moves(color):
            if mv == (r,c,nr,nc):
                legal = True
                break
        if not legal:
            return False

        state_snapshot = {
            'board': deepcopy(self.board),
            'white_to_move': self.white_to_move,
            'castling': deepcopy(self.castling),
            'en_passant': deepcopy(self.en_passant),
            'halfmove_clock': self.halfmove_clock,
            'fullmove_number': self.fullmove_number,
            'move': f"{r},{c}->{nr},{nc}"
        }
        self.move_history.append(state_snapshot)

        moving = self.board[r][c]
        target = self.board[nr][nc]
        # halfmove clock
        if moving.lower() == 'p' or target is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # en-passant capture: If moving pawn to en_passant and target square empty => captured pawn behind it
        if moving.lower() == 'p' and self.en_passant and (nr, nc) == self.en_passant and self.board[nr][nc] is None:
            # captured pawn is on the rank behind en_passant square relative to mover
            cap_r = nr - (1 if moving.isupper() else -1)
            cap_c = nc
            if self.in_bounds(cap_r, cap_c):
                self.board[cap_r][cap_c] = None

        # castling
        if moving.lower() == 'k' and abs(nc - c) == 2:
            if nc == 6:
                if moving.isupper():
                    # white kingside
                    self.board[0][7] = None
                    self.board[0][5] = 'R'
                else:
                    self.board[7][7] = None
                    self.board[7][5] = 'r'
            else:
                if moving.isupper():
                    self.board[0][0] = None
                    self.board[0][3] = 'R'
                else:
                    self.board[7][0] = None
                    self.board[7][3] = 'r'

        # move piece
        self.board[nr][nc] = self.board[r][c]
        self.board[r][c] = None

        # update castling rights
        if moving == 'K':
            self.castling[0] = False; self.castling[1] = False
        if moving == 'k':
            self.castling[2] = False; self.castling[3] = False
        if (r,c) == (0,0) or (nr,nc) == (0,0):
            self.castling[1] = False
        if (r,c) == (0,7) or (nr,nc) == (0,7):
            self.castling[0] = False
        if (r,c) == (7,0) or (nr,nc) == (7,0):
            self.castling[3] = False
        if (r,c) == (7,7) or (nr,nc) == (7,7):
            self.castling[2] = False

        # set en-passant target if pawn moved two
        self.en_passant = None
        if moving.lower() == 'p' and abs(nr - r) == 2:
            ep_r = (r + nr) // 2
            ep_c = c
            self.en_passant = (ep_r, ep_c)

        # promotion
        if self.board[nr][nc] == 'P' and nr == 7:
            choice = promotion_choice or 'Q'
            self.board[nr][nc] = choice.upper()
        if self.board[nr][nc] == 'p' and nr == 0:
            choice = promotion_choice or 'q'
            self.board[nr][nc] = choice.lower()

        # toggle side and fullmove number
        self.white_to_move = not self.white_to_move
        if not self.white_to_move:
            self.fullmove_number += 1
        return True

    def undo_move(self):
        if not self.move_history:
            return False
        last = self.move_history.pop()
        self.board = last['board']
        self.white_to_move = last['white_to_move']
        self.castling = last['castling']
        self.en_passant = last['en_passant']
        self.halfmove_clock = last['halfmove_clock']
        self.fullmove_number = last['fullmove_number']
        return True

    def to_json(self):
        data = {
            'board': self.board,
            'white_to_move': self.white_to_move,
            'castling': self.castling,
            'en_passant': self.en_passant,
            'move_history': self.move_history,
            'halfmove_clock': self.halfmove_clock,
            'fullmove_number': self.fullmove_number
        }
        return json.dumps(data)

    def load_json(self, s):
        data = json.loads(s)
        self.board = data['board']
        self.white_to_move = data['white_to_move']
        self.castling = data['castling']
        self.en_passant = tuple(data['en_passant']) if data.get('en_passant') is not None else None
        self.move_history = data.get('move_history', [])
        self.halfmove_clock = data.get('halfmove_clock', 0)
        self.fullmove_number = data.get('fullmove_number', 1)


# Simple AI implementations
PIECE_VALUE = {'p':1,'n':3,'b':3,'r':5,'q':9,'k':1000}

def evaluate_board(gs: GameState):
    score = 0
    for r in range(8):
        for c in range(8):
            p = gs.board[r][c]
            if p is None: continue
            v = PIECE_VALUE.get(p.lower(), 0)
            if p.isupper(): score += v
            else: score -= v
    w_moves = len(gs.generate_legal_moves('white'))
    b_moves = len(gs.generate_legal_moves('black'))
    score += 0.05 * (w_moves - b_moves)
    return score

def minimax(gs: GameState, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate_board(gs), None
    color = 'white' if maximizing else 'black'
    moves = gs.generate_legal_moves(color)
    if not moves:
        in_check = gs.is_in_check(color)
        if in_check:
            return (-9999 if maximizing else 9999), None
        return 0, None
    best_move = None
    if maximizing:
        max_eval = -math.inf
        for mv in moves:
            r,c,nr,nc = mv
            child = deepcopy(gs)
            moving_piece = child.board[r][c]
            promo = None
            if moving_piece and moving_piece.lower() == 'p':
                if moving_piece.isupper() and nr == 7: promo = 'Q'
                if moving_piece.islower() and nr == 0: promo = 'q'
            child.make_move(r,c,nr,nc,promotion_choice=promo)
            val, _ = minimax(child, depth-1, alpha, beta, False)
            if val > max_eval:
                max_eval = val; best_move = mv
            alpha = max(alpha, val)
            if beta <= alpha: break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for mv in moves:
            r,c,nr,nc = mv
            child = deepcopy(gs)
            moving_piece = child.board[r][c]
            promo = None
            if moving_piece and moving_piece.lower() == 'p':
                if moving_piece.isupper() and nr == 7: promo = 'Q'
                if moving_piece.islower() and nr == 0: promo = 'q'
            child.make_move(r,c,nr,nc,promotion_choice=promo)
            val, _ = minimax(child, depth-1, alpha, beta, True)
            if val < min_eval:
                min_eval = val; best_move = mv
            beta = min(beta, val)
            if beta <= alpha: break
        return min_eval, best_move

def ai_choose_move(gs: GameState, level='easy', side='black'):
    moves = gs.generate_legal_moves(side)
    if not moves: return None
    if level == 'easy':
        return random.choice(moves)
    if level == 'medium':
        scored = []
        for mv in moves:
            r,c,nr,nc = mv
            score = 0
            if gs.board[nr][nc] is not None:
                score += 10 * PIECE_VALUE.get(gs.board[nr][nc].lower(),1)
            # prefer center
            score -= (abs(3.5 - nr) + abs(3.5 - nc))
            scored.append((score, mv))
        scored.sort(reverse=True, key=lambda x: x[0])
        top = [mv for s,mv in scored[:max(1,len(scored)//3)]]
        return random.choice(top)
    # hard: use minimax with depth 2 or 3 depending on performance
    maximizing = True if side == 'white' else False
    depth = 2
    _, mv = minimax(gs, depth, -math.inf, math.inf, maximizing)
    if mv is None:
        return random.choice(moves)
    return mv


class ChessGUI:
    def __init__(self, root):
        self.root = root
        root.title("Full Python Chess")
        self.state = GameState()
        self.selected = None
        self.buttons = [[None]*8 for _ in range(8)]
        # mode settings initialized, will be set by the startup modal
        self.ai_enabled = False
        self.ai_side = 'black'
        self.ai_level = 'easy'
        self.game_over = False
        self.after_id = None
        self.move_listbox = None

        # Ask user for mode / side choice
        self.startup_modal()

        self.build_ui()
        self.draw_board()

        # If AI should move first, schedule it
        if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
            self.schedule_ai_move()

    def startup_modal(self):
        # Create a modal dialog to choose mode & side
        modal = tk.Toplevel(self.root)
        modal.title("Game Setup")
        modal.transient(self.root)
        modal.grab_set()
        tk.Label(modal, text="Choose Mode:").pack(anchor='w', padx=8, pady=(8,0))
        mode_var = tk.StringVar(value='Human vs AI')
        tk.Radiobutton(modal, text='Human vs Human', variable=mode_var, value='Human vs Human').pack(anchor='w', padx=16)
        tk.Radiobutton(modal, text='Human vs AI', variable=mode_var, value='Human vs AI').pack(anchor='w', padx=16)

        tk.Label(modal, text="If Human vs AI — choose your side:").pack(anchor='w', padx=8, pady=(8,0))
        side_var = tk.StringVar(value='white')
        tk.Radiobutton(modal, text='Play White (move first)', variable=side_var, value='white').pack(anchor='w', padx=16)
        tk.Radiobutton(modal, text='Play Black (move second)', variable=side_var, value='black').pack(anchor='w', padx=16)

        tk.Label(modal, text="AI Level:").pack(anchor='w', padx=8, pady=(8,0))
        level_var = tk.StringVar(value='easy')
        tk.Radiobutton(modal, text='Easy', variable=level_var, value='easy').pack(anchor='w', padx=16)
        tk.Radiobutton(modal, text='Medium', variable=level_var, value='medium').pack(anchor='w', padx=16)
        tk.Radiobutton(modal, text='Hard', variable=level_var, value='hard').pack(anchor='w', padx=16)

        btn_frame = tk.Frame(modal)
        btn_frame.pack(fill='x', pady=8)
        def on_ok():
            mode = mode_var.get()
            if mode == 'Human vs Human':
                self.ai_enabled = False
            else:
                self.ai_enabled = True
                self.ai_side = 'black' if side_var.get() == 'black' else 'white'
                self.ai_level = level_var.get()
            modal.grab_release()
            modal.destroy()

        def on_cancel():
            # default to Human vs AI black easy
            self.ai_enabled = True
            self.ai_side = 'black'
            self.ai_level = 'easy'
            modal.grab_release()
            modal.destroy()

        tk.Button(btn_frame, text='OK', command=on_ok).pack(side='left', padx=8)
        tk.Button(btn_frame, text='Cancel', command=on_cancel).pack(side='right', padx=8)

        self.root.wait_window(modal)

    def build_ui(self):
        top = tk.Frame(self.root)
        top.pack()
        board_frame = tk.Frame(top)
        board_frame.grid(row=0, column=0)
        for r in range(8):
            for c in range(8):
                btn = tk.Button(board_frame, text='', font=('Helvetica', 32), width=2, height=1,
                                command=lambda rr=r, cc=c: self.on_click(rr,cc))
                # visual orientation: row 7 at top of grid -> so invert when placing
                btn.grid(row=7-r, column=c)
                self.buttons[r][c] = btn
        ctrl = tk.Frame(top)
        ctrl.grid(row=0, column=1, padx=8)
        tk.Label(ctrl, text='Mode').pack()
        self.mode_var = tk.StringVar(value='Human vs AI' if self.ai_enabled else 'Human vs Human')
        for m in ['Human vs Human','Human vs AI']:
            tk.Radiobutton(ctrl, text=m, variable=self.mode_var, value=m, command=self.on_mode_change).pack(anchor='w')
        tk.Label(ctrl, text='AI Side').pack()
        self.ai_side_var = tk.StringVar(value=self.ai_side)
        for s in [('Black','black'),('White','white')]:
            tk.Radiobutton(ctrl, text=s[0], variable=self.ai_side_var, value=s[1], command=self.on_mode_change).pack(anchor='w')
        tk.Label(ctrl, text='AI Level').pack()
        self.ai_level_var = tk.StringVar(value=self.ai_level)
        for lv in [('Easy','easy'),('Medium','medium'),('Hard','hard')]:
            tk.Radiobutton(ctrl, text=lv[0], variable=self.ai_level_var, value=lv[1], command=self.on_mode_change).pack(anchor='w')

        tk.Button(ctrl, text='Undo', command=self.undo).pack(fill='x', pady=2)
        tk.Button(ctrl, text='Restart', command=self.restart).pack(fill='x', pady=2)
        tk.Button(ctrl, text='Save', command=self.save_game).pack(fill='x', pady=2)
        tk.Button(ctrl, text='Load', command=self.load_game).pack(fill='x', pady=2)
        # Move history box
        tk.Label(ctrl, text='Move History').pack(pady=(8, 0))
        self.move_listbox = tk.Listbox(ctrl, width=25, height=15)
        self.move_listbox.pack(fill='both', expand=True)


        self.status = tk.Label(self.root, text='White to move')
        self.status.pack()

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == 'Human vs AI':
            self.ai_enabled = True
            self.ai_side = self.ai_side_var.get()
            self.ai_level = self.ai_level_var.get()
            # If AI to move now, schedule
            if (self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move):
                self.schedule_ai_move()
        else:
            self.ai_enabled = False
            if self.after_id:
                try: self.root.after_cancel(self.after_id)
                except: pass
                self.after_id = None

    def draw_board(self):
        for r in range(8):
            for c in range(8):
                piece = self.state.board[r][c]
                btn = self.buttons[r][c]
                txt = PIECE_UNICODE.get(piece, '') if piece else ''
                btn.config(text=txt)
                bg = '#EEEED2' if (r+c)%2==0 else '#769656'
                btn.config(bg=bg, activebackground=bg, relief='raised')
        self.update_status()

    def on_click(self, r, c):
        if self.game_over:
            messagebox.showinfo('Game Over','The game is over. Restart to play again.')
            return
        # if AI is to move, ignore clicks
        if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
            return

        piece = self.state.board[r][c]
        side = 'white' if self.state.white_to_move else 'black'
        if self.selected is None:
            if piece is None:
                return
            if self.state.ally(piece) != side:
                messagebox.showerror('Invalid Selection','That is not your piece.')
                return
            self.selected = (r,c)
            self.highlight_moves(r,c)
            return
        sr, sc = self.selected
        moving_piece = self.state.board[sr][sc]
        will_promote = False
        if moving_piece and moving_piece.lower() == 'p':
            # promotion happens when pawn moves into last rank
            if moving_piece.isupper() and r == 7: will_promote = True
            if moving_piece.islower() and r == 0: will_promote = True
        promo_choice = None
        if will_promote:
            promo = simpledialog.askstring('Promotion','Promote to (Q,R,B,N):',parent=self.root)
            if promo and promo[0].upper() in ('Q','R','B','N'):
                promo_choice = promo[0].upper()
                if moving_piece.islower(): promo_choice = promo_choice.lower()
            else:
                promo_choice = 'q' if moving_piece.islower() else 'Q'
        moved = self.state.make_move(sr, sc, r, c, promotion_choice=promo_choice)
        self.selected = None
        self.clear_highlights()
        if not moved:
            messagebox.showerror('Invalid Move', 'That move is not legal.')
            # if user clicked on their own piece, allow reselect
            if piece is not None and self.state.ally(piece) == side:
                self.selected = (r,c)
                self.highlight_moves(r,c)
            else:
                self.root.bell()
            return
        # successful move
        self.draw_board()
        self.check_post_move()
                # Log move to move history box
        last_move = self.state.move_history[-1]['move']
        self.move_listbox.insert(tk.END, f"{len(self.state.move_history)}. {last_move}")
        self.move_listbox.yview(tk.END)


        # schedule AI if needed
        if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
            self.schedule_ai_move()

    def highlight_moves(self, r, c):
        self.clear_highlights()
        piece = self.state.board[r][c]
        if piece is None: return
        color = 'white' if piece.isupper() else 'black'
        if (color == 'white') != self.state.white_to_move:
            return
        moves = self.state.generate_legal_moves(color)
        for sr, sc, nr, nc in moves:
            if sr == r and sc == c:
                btn = self.buttons[nr][nc]
                btn.config(bg='#BACA2B')
        self.buttons[r][c].config(bg='#F6F669', relief='sunken')

    def clear_highlights(self):
        for r in range(8):
            for c in range(8):
                bg = '#EEEED2' if (r+c)%2==0 else '#769656'
                self.buttons[r][c].config(bg=bg, relief='raised')

    def update_status(self):
        if self.game_over:
            self.status.config(text=self.game_over if isinstance(self.game_over, str) else 'Game Over')
            return
        to_move = 'White' if self.state.white_to_move else 'Black'
        self.status.config(text=f"{to_move} to move | Fullmove: {self.state.fullmove_number} | Halfmove clock: {self.state.halfmove_clock}")

    def undo(self):
        ok = self.state.undo_move()
        if not ok:
            messagebox.showinfo('Undo','Nothing to undo')
        else:
            self.game_over = False
            self.selected = None
            self.draw_board()
            # Remove last move from history
            if self.move_listbox.size() > 0:
                self.move_listbox.delete(tk.END)

            if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
                self.schedule_ai_move()

    def restart(self):
        self.state = GameState()
        self.selected = None
        self.game_over = False
        self.draw_board()
        # if AI should move first
        if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
            self.schedule_ai_move()

    def save_game(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON','*.json')])
        if not path: return
        try:
            with open(path,'w') as f:
                f.write(self.state.to_json())
            messagebox.showinfo('Save','Game saved')
        except Exception as e:
            messagebox.showerror('Error',str(e))

    def load_game(self):
        path = filedialog.askopenfilename(filetypes=[('JSON','*.json')])
        if not path: return
        try:
            with open(path,'r') as f:
                s = f.read()
            self.state = GameState()
            self.state.load_json(s)
            self.selected = None
            self.game_over = False
            self.draw_board()
            messagebox.showinfo('Load','Game loaded')
            if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
                self.schedule_ai_move()
        except Exception as e:
            messagebox.showerror('Error',str(e))

    def schedule_ai_move(self):
        if self.after_id:
            try: self.root.after_cancel(self.after_id)
            except: pass
        # slight pause so UI updates show and for user to see messages
        self.after_id = self.root.after(300, self.do_ai_move)

    def do_ai_move(self):
        if self.game_over:
            return
        self.ai_side = self.ai_side_var.get()
        self.ai_level = self.ai_level_var.get()
        side = 'white' if self.state.white_to_move else 'black'
        if side != self.ai_side:
            return
        mv = ai_choose_move(self.state, level=self.ai_level, side=side)
        if mv is None:
            # no moves -> handle below
            self.check_post_move(force_check_current=True)
            return
        r,c,nr,nc = mv
        promo = None
        moving = self.state.board[r][c]
        if moving and moving.lower() == 'p':
            if moving.isupper() and nr == 7: promo = 'Q'
            if moving.islower() and nr == 0: promo = 'q'
        self.state.make_move(r,c,nr,nc,promotion_choice=promo)
        self.draw_board()
        self.check_post_move()
        return

    def check_post_move(self, force_check_current=False):
        """
        After a move (or when AI has no moves), determine:
        - if the side to move is in check,
        - if there are legal moves for side to move and handle checkmate/stalemate,
        - set game_over and show appropriate dialogs.
        If force_check_current=True, we evaluate the current side to move even if no one moved (used for AI no-move case).
        """
        side_to_move = 'white' if self.state.white_to_move else 'black'
        legal_moves = self.state.generate_legal_moves(side_to_move)
        in_check = self.state.is_in_check(side_to_move)

        # No legal moves -> checkmate or stalemate
        if not legal_moves:
            if in_check:
                # checkmate: the side to move is checkmated, so opponent wins
                winner = "White" if side_to_move == "black" else "Black"
                messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
                self.game_over = True
            else:
                # stalemate
                messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
                self.game_over = True
            self.update_status()
            return

        # If there are legal moves and side is in check -> notify check
        if in_check:
            messagebox.showinfo("Check", f"{side_to_move.capitalize()} is in check!")

        # Normal ongoing game
        self.game_over = False
        self.update_status()
        return


if __name__ == '__main__':
    root = tk.Tk()
    gui = ChessGUI(root)
    gui.root.geometry('800x520')
    root.mainloop()
