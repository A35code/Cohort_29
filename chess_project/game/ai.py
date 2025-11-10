import random, math
from copy import deepcopy
from .state import GameState
from .utilities import PIECE_VALUE

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
            score -= (abs(3.5 - nr) + abs(3.5 - nc))
            scored.append((score, mv))
        scored.sort(reverse=True, key=lambda x: x[0])
        top = [mv for s,mv in scored[:max(1,len(scored)//3)]]
        return random.choice(top)
    maximizing = True if side == 'white' else False
    depth = 2
    _, mv = minimax(gs, depth, -math.inf, math.inf, maximizing)
    if mv is None:
        return random.choice(moves)
    return mv
