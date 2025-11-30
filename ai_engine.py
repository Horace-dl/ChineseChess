from rule_mgr import RuleMgr
from piece_point import PiecePoint
import math
import time
from collections import namedtuple


PIECE_VALUES = {
    'General': 10000,
    'Marshal': 10000,
    'Rook': 900,
    'Cannon': 450,
    'Knight': 300,
    'Minister': 300,
    'Guard': 200,
    'Soldier': 100
}

# Simple piece-square tables (small positional bonuses). Keys are piece names.
PIECE_SQUARES = {
    'Soldier':  [0]*256,  # placeholder, unused granularly
}

# Transposition table entry
TTEntry = namedtuple('TTEntry', ['depth', 'value', 'flag', 'best_move'])
# flags: 'EXACT', 'LOWER', 'UPPER'

# Simple global transposition table (cleared per top-level search)
_TT = {}



def evaluate(piece_list):
    """Simple material evaluation: positive means advantage for RED, negative for BLACK."""
    score = 0
    # material
    for p in piece_list:
        try:
            if p.get_status() != 0:
                continue
            val = PIECE_VALUES.get(p.get_name(), 0)
            if p.get_type() == 'RED':
                score += val
            else:
                score -= val
        except Exception:
            continue

    # Additional lightweight heuristics could be added here (mobility, central control).
    return score


def generate_moves(rule_mgr: RuleMgr, player_type: str):
    """Yield moves as tuples (piece, dest_pos, captured_piece_or_None)."""
    moves = []
    for pc in rule_mgr._piece_list:
        try:
            if pc.get_status() != 0:
                continue
            if pc.get_type() != player_type:
                continue
            pid = getattr(pc, '_id', None)
            possible = rule_mgr.get_possible_pos(pc.get_type(), pid)
        except Exception:
            continue

        for dest in possible:
            # determine if there's a piece occupying dest
            captured = None
            for t in rule_mgr._piece_list:
                try:
                    if t.position.pos_x == dest.pos_x and t.position.pos_y == dest.pos_y and t.get_status() == 0:
                        captured = t
                        break
                except Exception:
                    continue

            # validate candidate with rule manager
            try:
                if captured is None:
                    ok = rule_mgr.check_move(pc, dest)
                    if not ok:
                        continue
                else:
                    ok, _ = rule_mgr.check_knock_over(pc, captured)
                    if not ok:
                        continue
            except Exception:
                # if validation throws for some reason, skip this candidate
                continue

            moves.append((pc, dest, captured))

    # Move ordering: captures first using an MVV-LVA-like heuristic
    def mvv_lva_key(mv):
        attacker = mv[0]
        victim = mv[2]
        if victim is None:
            return 0
        try:
            return PIECE_VALUES.get(victim.get_name(), 0) * 1000 - PIECE_VALUES.get(attacker.get_name(), 0)
        except Exception:
            return 0

    moves.sort(key=mvv_lva_key, reverse=True)
    return moves


def make_move(move):
    """Apply move in-place. Return rollback info to restore state."""
    piece, dest, captured = move
    prev_pos = PiecePoint(piece.position.pos_x, piece.position.pos_y)
    prev_status_captured = None
    if captured is not None:
        prev_status_captured = (captured, PiecePoint(captured.position.pos_x, captured.position.pos_y), captured.get_status())
        captured.set_status(1)
        captured.set_position(PiecePoint(0, 0))
    piece.set_position(dest)
    return (piece, prev_pos, prev_status_captured)


def undo_move(rollback_info):
    piece, prev_pos, prev_status_captured = rollback_info
    piece.set_position(prev_pos)
    if prev_status_captured is not None:
        cap, pos, status = prev_status_captured
        cap.set_status(status)
        cap.set_position(pos)


def alpha_beta(rule_mgr: RuleMgr, depth: int, maximizing_player: bool, alpha=-math.inf, beta=math.inf):
    """Alpha-beta search. Returns (best_score, best_move) where best_move is (piece,dest,captured) or None.

    The search modifies the shared piece list in RuleMgr and restores moves on undo.
    """
    # enhanced search: iterative deepening + quiescence + transposition table
    _TT.clear()

    def position_key():
        try:
            lst = []
            for p in rule_mgr._piece_list:
                try:
                    lst.append((getattr(p, '_id', None), p.get_name(), p.get_type(), p.position.pos_x, p.position.pos_y, p.get_status()))
                except Exception:
                    continue
            lst.sort()
            return tuple(lst)
        except Exception:
            return None

    def quiescence(a, b, maximizing):
        stand_pat = evaluate(rule_mgr._piece_list)
        if maximizing:
            if stand_pat >= b:
                return b
            if a < stand_pat:
                a = stand_pat
        else:
            if stand_pat <= a:
                return a
            if b > stand_pat:
                b = stand_pat

        player = 'RED' if maximizing else 'BLACK'
        captures = [m for m in generate_moves(rule_mgr, player) if m[2] is not None]
        for m in captures:
            rb = make_move(m)
            score = quiescence(a, b, not maximizing)
            undo_move(rb)
            if maximizing:
                if score > a:
                    a = score
                if a >= b:
                    return b
            else:
                if score < b:
                    b = score
                if a >= b:
                    return a

        return a if maximizing else b

    def _search(d, maximizing, a, b):
        key = position_key()
        if key is not None and key in _TT:
            entry = _TT[key]
            if entry.depth >= d:
                if entry.flag == 'EXACT':
                    return entry.value, entry.best_move
                elif entry.flag == 'LOWER' and entry.value > a:
                    a = entry.value
                elif entry.flag == 'UPPER' and entry.value < b:
                    b = entry.value

        if d == 0:
            val = quiescence(a, b, maximizing)
            return val, None

        player = 'RED' if maximizing else 'BLACK'
        moves = generate_moves(rule_mgr, player)
        if not moves:
            return evaluate(rule_mgr._piece_list), None

        best_move = None
        if maximizing:
            value = -math.inf
            for m in moves:
                rb = make_move(m)
                score, _ = _search(d - 1, False, a, b)
                undo_move(rb)
                if score > value:
                    value = score
                    best_move = m
                a = max(a, value)
                if a >= b:
                    break
            if key is not None:
                flag = 'EXACT'
                if value <= alpha:
                    flag = 'UPPER'
                elif value >= beta:
                    flag = 'LOWER'
                _TT[key] = TTEntry(d, value, flag, best_move)
            return value, best_move
        else:
            value = math.inf
            for m in moves:
                rb = make_move(m)
                score, _ = _search(d - 1, True, a, b)
                undo_move(rb)
                if score < value:
                    value = score
                    best_move = m
                b = min(b, value)
                if a >= b:
                    break
            if key is not None:
                flag = 'EXACT'
                if value <= alpha:
                    flag = 'UPPER'
                elif value >= beta:
                    flag = 'LOWER'
                _TT[key] = TTEntry(d, value, flag, best_move)
            return value, best_move

    # iterative deepening
    best = None
    best_score = None
    for d in range(1, max(1, depth) + 1):
        try:
            _TT.clear()
            score, mv = _search(d, maximizing_player, alpha, beta)
            if mv is not None:
                best = mv
                best_score = score
        except Exception:
            break

    return (best_score if best_score is not None else evaluate(rule_mgr._piece_list)), best
