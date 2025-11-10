from copy import deepcopy
import json

from .utilities import FILES

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
        b = [[None for _ in range(8)] for _ in range(8)]
        for c in range(8):
            b[1][c] = 'P'
            b[6][c] = 'p'
        b[0][0] = b[0][7] = 'R'
        b[0][1] = b[0][6] = 'N'
        b[0][2] = b[0][5] = 'B'
        b[0][3] = 'Q'
        b[0][4] = 'K'
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
            for dc in (-1, 1):
                fc = c + dc
                if self.in_bounds(fr, fc):
                    target = self.board[fr][fc]
                    if target is not None and self.ally(target) != color:
                        moves.append((fr, fc))
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
            if color == 'white' and r == 0 and c == 4:
                if self.castling[0] and self.board[0][5] is None and self.board[0][6] is None:
                    if not self.is_in_check('white') and not self.square_under_attack((0,5),'white') and not self.square_under_attack((0,6),'white'):
                        moves.append((0,6))
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
                    if moving and moving.lower() == 'p' and self.en_passant and (nr, nc) == self.en_passant and new_board[nr][nc] is None:
                        capture_r = r
                        capture_c = nc
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
        if moving.lower() == 'p' or target is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if moving.lower() == 'p' and self.en_passant and (nr, nc) == self.en_passant and self.board[nr][nc] is None:
            cap_r = nr - (1 if moving.isupper() else -1)
            cap_c = nc
            if self.in_bounds(cap_r, cap_c):
                self.board[cap_r][cap_c] = None

        if moving.lower() == 'k' and abs(nc - c) == 2:
            if nc == 6:
                if moving.isupper():
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

        self.board[nr][nc] = self.board[r][c]
        self.board[r][c] = None

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

        self.en_passant = None
        if moving.lower() == 'p' and abs(nr - r) == 2:
            ep_r = (r + nr) // 2
            ep_c = c
            self.en_passant = (ep_r, ep_c)

        if self.board[nr][nc] == 'P' and nr == 7:
            choice = promotion_choice or 'Q'
            self.board[nr][nc] = choice.upper()
        if self.board[nr][nc] == 'p' and nr == 0:
            choice = promotion_choice or 'q'
            self.board[nr][nc] = choice.lower()

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
