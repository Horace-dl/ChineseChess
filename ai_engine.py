from rule_mgr import RuleMgr
from piece_point import PiecePoint
import math
import time
from collections import namedtuple
import random


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

# Piece-square tables (9 files x 10 ranks = 90 entries) - values in centipawns
PIECE_SQUARES = {
    # Rook (encourage central files and open ranks)
    'Rook': [
        10, 10, 15, 20, 20, 20, 15, 10, 10,
        10, 12, 18, 22, 25, 22, 18, 12, 10,
        8,  10, 15, 18, 20, 18, 15, 10, 8,
        6,  8,  12, 15, 16, 15, 12, 8, 6,
        4,  6,  8,  10, 12, 10, 8, 6, 4,
        4,  6,  8,  10, 12, 10, 8, 6, 4,
        6,  8,  12, 15, 16, 15, 12, 8, 6,
        8,  10, 15, 18, 20, 18, 15, 10, 8,
        10, 12, 18, 22, 25, 22, 18, 12, 10,
        10, 10, 15, 20, 20, 20, 15, 10, 10,
    ],
    # Cannon (similar to rook but slightly less)
    'Cannon': [
        8, 8, 12, 16, 18, 16, 12, 8, 8,
        8, 10, 14, 18, 20, 18, 14, 10, 8,
        6, 8, 12, 15, 16, 15, 12, 8, 6,
        4, 6, 8, 10, 12, 10, 8, 6, 4,
        2, 4, 6, 8, 10, 8, 6, 4, 2,
        2, 4, 6, 8, 10, 8, 6, 4, 2,
        4, 6, 8, 10, 12, 10, 8, 6, 4,
        6, 8, 12, 15, 16, 15, 12, 8, 6,
        8, 10, 14, 18, 20, 18, 14, 10, 8,
        8, 8, 12, 16, 18, 16, 12, 8, 8,
    ],
    # Knight (prefer central squares)
    'Knight': [
        4, 4, 6, 8, 8, 8, 6, 4, 4,
        4, 6, 8, 10, 12, 10, 8, 6, 4,
        3, 6, 9, 12, 14, 12, 9, 6, 3,
        2, 4, 8, 10, 12, 10, 8, 4, 2,
        1, 2, 4, 6, 8, 6, 4, 2, 1,
        1, 2, 4, 6, 8, 6, 4, 2, 1,
        2, 4, 8, 10, 12, 10, 8, 4, 2,
        3, 6, 9, 12, 14, 12, 9, 6, 3,
        4, 6, 8, 10, 12, 10, 8, 6, 4,
        4, 4, 6, 8, 8, 8, 6, 4, 4,
    ],
    # Soldier: encourage forward ranks and central files
    'Soldier': [
        0, 0, 2, 3, 3, 3, 2, 0, 0,
        1, 1, 3, 4, 5, 4, 3, 1, 1,
        2, 2, 4, 6, 6, 6, 4, 2, 2,
        3, 3, 5, 7, 8, 7, 5, 3, 3,
        4, 4, 6, 8,10, 8, 6, 4, 4,
        4, 4, 6, 8,10, 8, 6, 4, 4,
        3, 3, 5, 7, 8, 7, 5, 3, 3,
        2, 2, 4, 6, 6, 6, 4, 2, 2,
        1, 1, 3, 4, 5, 4, 3, 1, 1,
        0, 0, 2, 3, 3, 3, 2, 0, 0,
    ],
    # Marshal/General: keep small center preference
    'Marshal': [
        0,0,0,1,1,1,0,0,0,
        0,0,1,2,2,2,1,0,0,
        0,0,1,2,3,2,1,0,0,
    ] * 3,
}

# Positional and mobility multipliers by piece type
PIECE_POSITION_FACTOR = {
    'General': 0,
    'Marshal': 8,
    'Rook': 14,
    'Cannon': 12,
    'Knight': 10,
    'Minister': 6,
    'Guard': 4,
    'Soldier': 6,
}

# Mobility weight per move by piece type (how valuable an extra legal move is)
MOBILITY_WEIGHT_BY_PIECE = {
    'General': 0,
    'Marshal': 12,
    'Rook': 18,
    'Cannon': 16,
    'Knight': 14,
    'Minister': 8,
    'Guard': 4,
    'Soldier': 6,
}

# Tunable evaluation weights
CAPTURE_WEIGHT = 180
CHECK_PENALTY = 5000

def _positional_bonus(piece):
    """Compute a small positional bonus based on centrality and rank.

    Uses board coordinates where x in [0..8], y in [0..9]. Values are symmetric for BLACK via mirroring.
    """
    try:
        x = int(piece.position.pos_x)
        y = int(piece.position.pos_y)
    except Exception:
        return 0

    # centrality: center file is x=4
    cx = 4
    centrality = max(0, 4 - abs(cx - x))  # 0..4
    # rank bonus: encourage advanced soldiers (for RED smaller y -> forward?), we keep symmetric
    cy = 4.5
    rank_central = int(max(0, 5 - abs(cy - y)))  # 0..5

    name = piece.get_name()
    # use piece-square table if available (mirror for BLACK)
    try:
        table = PIECE_SQUARES.get(name)
        if table:
            x = int(piece.position.pos_x)
            y = int(piece.position.pos_y)
            # mirror y for BLACK so same table works for both sides
            if piece.get_type() == 'BLACK':
                y = 9 - y
            idx = y * 9 + x
            if 0 <= idx < len(table):
                return table[idx]
    except Exception:
        pass

    base = (centrality * 8) + (rank_central * 4)
    factor = PIECE_POSITION_FACTOR.get(name, 1)
    return base * factor

def _mobility_score(rule_mgr: RuleMgr):
    """Compute mobility score as weighted sum of legal moves per piece type (RED - BLACK).

    Returns an integer to be added to evaluation (positive favors RED).
    """
    try:
        red_counts = {k: 0 for k in MOBILITY_WEIGHT_BY_PIECE}
        black_counts = {k: 0 for k in MOBILITY_WEIGHT_BY_PIECE}
        for mv in generate_moves(rule_mgr, 'RED'):
            try:
                attacker = mv[0]
                name = attacker.get_name()
                red_counts[name] = red_counts.get(name, 0) + 1
            except Exception:
                continue
        for mv in generate_moves(rule_mgr, 'BLACK'):
            try:
                attacker = mv[0]
                name = attacker.get_name()
                black_counts[name] = black_counts.get(name, 0) + 1
            except Exception:
                continue

        score = 0
        for name, weight in MOBILITY_WEIGHT_BY_PIECE.items():
            score += weight * (red_counts.get(name, 0) - black_counts.get(name, 0))
        return score
    except Exception:
        return 0

# Transposition table entry
TTEntry = namedtuple('TTEntry', ['depth', 'value', 'flag', 'best_move'])
# flags: 'EXACT', 'LOWER', 'UPPER'

# Simple global transposition table (cleared per top-level search)
_TT = {}

# Zobrist table (lazy-filled). Keys: (name, type, x, y) -> 64-bit int
_ZOBRIST = {}
# side key for BLACK to move (we XOR when BLACK to move)
_ZOBISTERSIDE = random.Random(0).getrandbits(64)



def evaluate(piece_list, rule_mgr: RuleMgr = None):
    """Material + lightweight positional evaluation.

    If `rule_mgr` is provided, also include mobility, capture opportunities, and king-safety
    heuristics that use legal-move generation.
    Positive score favors RED, negative favors BLACK.
    """
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

    # If rule_mgr available, add extra heuristics
    if rule_mgr is not None:
        try:
            # Per-piece positional bonuses
            pos_score = 0
            for p in piece_list:
                if getattr(p, 'get_status', lambda: 1)() != 0:
                    continue
                pos = _positional_bonus(p)
                if p.get_type() == 'RED':
                    pos_score += pos
                else:
                    pos_score -= pos
            score += pos_score

            # Mobility per-piece
            score += _mobility_score(rule_mgr)

            # Capture opportunities (how many captures available to each side)
            try:
                red_caps = sum(1 for m in generate_moves(rule_mgr, 'RED') if m[2] is not None)
                black_caps = sum(1 for m in generate_moves(rule_mgr, 'BLACK') if m[2] is not None)
                cap_diff = red_caps - black_caps
            except Exception:
                cap_diff = 0

            CAPTURE_WEIGHT = 40
            score += CAPTURE_WEIGHT * cap_diff

            # King safety: heavy penalty if in check
            try:
                if getattr(rule_mgr, 'is_in_check', None):
                    if rule_mgr.is_in_check('RED'):
                        score -= 3000
                    if rule_mgr.is_in_check('BLACK'):
                        score += 3000
            except Exception:
                pass

        except Exception:
            pass

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
    # Replace with Negamax + PVS + TT + killer & history heuristics
    _TT.clear()
    history = {}  # move_key -> score
    max_depth = max(1, depth)
    # simple killer table: killer[depth] = [move1, move2]
    killer = {d: [] for d in range(max_depth + 2)}

    def make_move_key(mv):
        try:
            pc, dest, cap = mv
            aid = getattr(pc, '_id', None)
            cid = getattr(cap, '_id', None) if cap is not None else None
            return (aid, dest.pos_x, dest.pos_y, cid)
        except Exception:
            return None

    # incremental evaluation helpers
    def _positional_bonus_xy(name, ptype, x, y):
        try:
            factor = PIECE_POSITION_FACTOR.get(name, 1)
            cx = 4
            centrality = max(0, 4 - abs(cx - int(x)))
            cy = 4.5
            rank_central = int(max(0, 5 - abs(cy - float(y))))
            base = (centrality * 8) + (rank_central * 4)
            return base * factor
        except Exception:
            return 0

    def quick_eval(piece_list):
        """Quick eval: material + positional bonuses (used for incremental updates)."""
        s = 0
        for p in (piece_list or []):
            try:
                if p.get_status() != 0:
                    continue
                val = PIECE_VALUES.get(p.get_name(), 0)
                pos = _positional_bonus(p)
                if p.get_type() == 'RED':
                    s += val + pos
                else:
                    s -= val + pos
            except Exception:
                continue
        return s

    def position_key():
        # Use Zobrist hashing for fast position keys. Lazy-generate random values for piece+square combos.
        try:
            h = 0
            for p in rule_mgr._piece_list:
                try:
                    if p.get_status() != 0:
                        continue
                    name = p.get_name()
                    ptype = p.get_type()
                    x = p.position.pos_x
                    y = p.position.pos_y
                    k = (name, ptype, x, y)
                    if k not in _ZOBRIST:
                        # deterministic random stream for reproducibility
                        _ZOBRIST[k] = random.Random(hash(k) & 0xffffffff).getrandbits(64)
                    h ^= _ZOBRIST[k]
                except Exception:
                    continue
            # XOR side key when BLACK to move
            # We determine side to move by counting pieces or relying on rule_mgr state if available.
            # If rule_mgr provides an attribute for current player, use it; otherwise assume RED to move.
            side = getattr(rule_mgr, 'current_player', None)
            if side is None:
                # fallback heuristic: if RED pieces > BLACK pieces -> BLACK to move next less likely
                # We won't attempt to compute side perfectly; if rule_mgr exposes state later, it will be used.
                side = None
            if side == 'BLACK':
                h ^= _ZOBISTERSIDE
            return h
        except Exception:
            return None

    # initialize incremental eval
    curr_eval = quick_eval(rule_mgr._piece_list)

    def do_move_incremental(move):
        """Apply move and return (rollback_info, delta) where delta is change to curr_eval."""
        piece, dest, captured = move
        # compute positional delta for mover
        try:
            pos_old = _positional_bonus(piece)
        except Exception:
            pos_old = 0
        try:
            pos_new = _positional_bonus_xy(piece.get_name(), piece.get_type(), dest.pos_x, dest.pos_y)
        except Exception:
            pos_new = 0

        delta = 0
        if piece.get_type() == 'RED':
            delta += (pos_new - pos_old)
        else:
            delta -= (pos_new - pos_old)

        # capture effect
        if captured is not None:
            try:
                cap_name = captured.get_name()
                cap_type = captured.get_type()
                cap_val = PIECE_VALUES.get(cap_name, 0)
                cap_pos = _positional_bonus(captured)
            except Exception:
                cap_val = 0
                cap_type = None
                cap_pos = 0

            if cap_type == 'RED':
                delta -= (cap_val + cap_pos)
            else:
                delta += (cap_val + cap_pos)

        rb = make_move(move)
        return rb, delta

    def undo_move_incremental(rollback_info, delta):
        # revert eval first, then revert piece state
        nonlocal curr_eval
        curr_eval -= delta
        undo_move(rollback_info)

    def qsearch(alpha, beta, color):
        # color: +1 for RED, -1 for BLACK
        nonlocal curr_eval
        # use incremental quick eval + a light check penalty (we don't recompute mobility here)
        stand = color * curr_eval
        if stand >= beta:
            return beta
        if alpha < stand:
            alpha = stand

        player = 'RED' if color == 1 else 'BLACK'
        caps = [m for m in generate_moves(rule_mgr, player) if m[2] is not None]
        for m in caps:
            rb, delta = do_move_incremental(m)
            curr_eval += delta
            score = -qsearch(-beta, -alpha, -color)
            undo_move_incremental(rb, delta)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha

    def tt_probe(key, depth, alpha, beta):
        if key is None:
            return None
        e = _TT.get(key)
        if e is None or e.depth < depth:
            return None
        if e.flag == 'EXACT':
            return e.value, e.best_move
        if e.flag == 'LOWER' and e.value >= beta:
            return e.value, e.best_move
        if e.flag == 'UPPER' and e.value <= alpha:
            return e.value, e.best_move
        return None

    def tt_store(key, depth, value, flag, best_move):
        if key is None:
            return
        _TT[key] = TTEntry(depth, value, flag, best_move)

    def order_moves(moves, depth, tt_best):
        # prioritize: TT best move, captures (MVV-LVA), killer moves, history
        def score_mv(mv):
            if tt_best is not None and mv == tt_best:
                return 1000000
            if mv[2] is not None:
                try:
                    return PIECE_VALUES.get(mv[2].get_name(), 0) * 1000 - PIECE_VALUES.get(mv[0].get_name(), 0)
                except Exception:
                    return 50000
            mk = make_move_key(mv)
            h = history.get(mk, 0)
            kl_score = 0
            for k in killer.get(depth, []):
                if k == mk:
                    kl_score += 2000
            return h + kl_score

        moves.sort(key=score_mv, reverse=True)
        return moves

    def negamax(node_depth, alpha, beta, color, ply=0):
        nonlocal curr_eval
        key = position_key()
        tt_hit = tt_probe(key, node_depth, alpha, beta)
        if tt_hit is not None:
            return tt_hit[0], tt_hit[1]

        if node_depth == 0:
            val = qsearch(alpha, beta, color)
            return val, None

        player = 'RED' if color == 1 else 'BLACK'
        moves = generate_moves(rule_mgr, player)
        if not moves:
            return color * evaluate(rule_mgr._piece_list, rule_mgr), None

        tt_best = None
        if key is not None:
            e = _TT.get(key)
            if e:
                tt_best = e.best_move

        moves = order_moves(moves, node_depth, tt_best)

        best_move = None
        first = True
        orig_alpha = alpha
        for m in moves:
            mk = make_move_key(m)
            rb, delta = do_move_incremental(m)
            curr_eval += delta
            if first:
                score, _ = negamax(node_depth - 1, -beta, -alpha, -color, ply + 1)
                score = -score
            else:
                # PVS / null-window search
                score, _ = negamax(node_depth - 1, -alpha - 1, -alpha, -color, ply + 1)
                score = -score
                if alpha < score < beta:
                    score, _ = negamax(node_depth - 1, -beta, -score, -color, ply + 1)
                    score = -score
            undo_move_incremental(rb, delta)

            if score >= beta:
                # store killer / history
                if mk is not None:
                    killer.setdefault(node_depth, [])
                    if mk not in killer[node_depth]:
                        killer[node_depth].insert(0, mk)
                        if len(killer[node_depth]) > 2:
                            killer[node_depth] = killer[node_depth][:2]
                tt_store(key, node_depth, score, 'LOWER', m)
                return score, m

            if score > alpha:
                alpha = score
                best_move = m
                # update history
                if mk is not None:
                    history[mk] = history.get(mk, 0) + (1 << node_depth)

            first = False

        # store result in TT
        flag = 'EXACT' if alpha != orig_alpha else 'UPPER'
        tt_store(key, node_depth, alpha, flag, best_move)
        return alpha, best_move

    # Time control: allow rule_mgr to specify `search_time_limit` (seconds). Fallback to 3s.
    start_time = time.time()
    time_limit = getattr(rule_mgr, 'search_time_limit', None)
    if time_limit is None:
        time_limit = 30.0

    class SearchTimeout(Exception):
        pass

    def _check_time():
        if time_limit is None:
            return
        if time.time() - start_time > time_limit:
            raise SearchTimeout()

    # inject time checks into search inner functions via closure
    orig_qsearch = qsearch
    def qsearch_with_time(alpha, beta, color):
        _check_time()
        return orig_qsearch(alpha, beta, color)

    # rebind qsearch used inside negamax
    qsearch = qsearch_with_time

    best = None
    best_score = None
    try:
        for d in range(1, max_depth + 1):
            _check_time()
            score, mv = negamax(d, alpha, beta, 1 if maximizing_player else -1)
            if mv is not None:
                best = mv
                best_score = score
    except SearchTimeout:
        # time's up: return the best move found from earlier completed depths
        pass
    except Exception:
        # other errors: stop and fall back to best we have
        pass

    return (best_score if best_score is not None else evaluate(rule_mgr._piece_list, rule_mgr)), best
