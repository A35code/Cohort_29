import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from copy import deepcopy

from game.state import GameState
from game.ai import ai_choose_move
from game.utilities import PIECE_UNICODE

class ChessGUI:
    def __init__(self, root):
        self.root = root
        root.title("Full Python Chess")
        self.state = GameState()
        self.selected = None
        self.buttons = [[None]*8 for _ in range(8)]
        self.ai_enabled = False
        self.ai_side = 'black'
        self.ai_level = 'easy'
        self.game_over = False
        self.after_id = None
        self.move_listbox = None

        self.startup_modal()

        self.build_ui()
        self.draw_board()

        if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
            self.schedule_ai_move()

    def startup_modal(self):
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
            if piece is not None and self.state.ally(piece) == side:
                self.selected = (r,c)
                self.highlight_moves(r,c)
            else:
                self.root.bell()
            return
        self.draw_board()
        self.check_post_move()
        last_move = self.state.move_history[-1]['move']
        self.move_listbox.insert(tk.END, f"{len(self.state.move_history)}. {last_move}")
        self.move_listbox.yview(tk.END)

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
            if self.move_listbox.size() > 0:
                self.move_listbox.delete(tk.END)

            if self.ai_enabled and ((self.ai_side == 'white' and self.state.white_to_move) or (self.ai_side == 'black' and not self.state.white_to_move)):
                self.schedule_ai_move()

    def restart(self):
        self.state = GameState()
        self.selected = None
        self.game_over = False
        self.draw_board()
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
        side_to_move = 'white' if self.state.white_to_move else 'black'
        legal_moves = self.state.generate_legal_moves(side_to_move)
        in_check = self.state.is_in_check(side_to_move)

        if not legal_moves:
            if in_check:
                winner = "White" if side_to_move == "black" else "Black"
                messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
                self.game_over = True
            else:
                messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
                self.game_over = True
            self.update_status()
            return

        if in_check:
            messagebox.showinfo("Check", f"{side_to_move.capitalize()} is in check!")

        self.game_over = False
        self.update_status()
        return
