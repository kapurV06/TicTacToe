"""
Streamlit UI for TicTacToe.
Run with:  streamlit run tictactoe_app.py
Requires:  pip install streamlit numpy
"""

import streamlit as st
import numpy as np
from hello import check_winner, is_draw, make_move, reset_board

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TicTacToe",
    page_icon="⚔️",
    layout="centered",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Share+Tech+Mono&display=swap');

    /* ---------- global ---------- */
    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0d0d;
        color: #e8e8e8;
        font-family: 'Share Tech Mono', monospace;
    }

    /* hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* ---------- title ---------- */
    .game-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(1.2rem, 4vw, 2rem);
        text-align: center;
        letter-spacing: 4px;
        margin: 1.6rem 0 0.4rem;
        color: #f0f0f0;
        text-shadow: 0 0 18px #ff4e50, 0 0 40px #ff4e5055;
    }

    /* ---------- status banner ---------- */
    .status-banner {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(0.55rem, 2vw, 0.75rem);
        text-align: center;
        padding: 10px 20px;
        border: 2px solid #ff4e50;
        border-radius: 4px;
        margin: 1rem auto;
        max-width: 420px;
        background: #1a1a1a;
        color: #ff4e50;
        box-shadow: 0 0 12px #ff4e5055;
        letter-spacing: 2px;
    }

    .status-banner.player-o {
        border-color: #00f0ff;
        color: #00f0ff;
        box-shadow: 0 0 12px #00f0ff55;
    }

    .status-banner.draw {
        border-color: #ffe74c;
        color: #ffe74c;
        box-shadow: 0 0 12px #ffe74c55;
    }

    /* ---------- board ---------- */
    .board-wrapper {
        display: flex;
        justify-content: center;
        margin: 1.2rem auto;
    }

    /* ---------- cell buttons ---------- */
    div[data-testid="stButton"] > button {
        font-family: 'Press Start 2P', monospace !important;
        font-size: clamp(1.4rem, 5vw, 2.4rem) !important;
        width: 110px !important;
        height: 110px !important;
        border: 2px solid #333 !important;
        border-radius: 6px !important;
        background: #1a1a1a !important;
        color: #e8e8e8 !important;
        transition: all 0.15s ease !important;
        margin: 3px !important;
        box-shadow: inset 0 0 0 0 transparent !important;
    }

    div[data-testid="stButton"] > button:hover:not(:disabled) {
        background: #242424 !important;
        border-color: #ff4e50 !important;
        box-shadow: 0 0 12px #ff4e5044 !important;
        transform: scale(1.04) !important;
    }

    div[data-testid="stButton"] > button:disabled {
        opacity: 1 !important;
        cursor: default !important;
    }

    /* color X cells red-ish */
    .x-cell > div[data-testid="stButton"] > button {
        color: #ff4e50 !important;
        text-shadow: 0 0 10px #ff4e50aa !important;
        border-color: #ff4e5066 !important;
    }

    /* color O cells cyan */
    .o-cell > div[data-testid="stButton"] > button {
        color: #00f0ff !important;
        text-shadow: 0 0 10px #00f0ffaa !important;
        border-color: #00f0ff66 !important;
    }

    /* ---------- scoreboard ---------- */
    .score-row {
        display: flex;
        justify-content: center;
        gap: 18px;
        margin: 0.6rem 0 1rem;
        flex-wrap: wrap;
    }

    .score-card {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6rem;
        padding: 10px 20px;
        border-radius: 4px;
        text-align: center;
        letter-spacing: 1px;
        min-width: 80px;
    }

    .score-card.x { background:#1f0d0d; border:2px solid #ff4e50; color:#ff4e50; }
    .score-card.o { background:#0d1f22; border:2px solid #00f0ff; color:#00f0ff; }
    .score-card.d { background:#1f1d0d; border:2px solid #ffe74c; color:#ffe74c; }

    /* ---------- reset button ---------- */
    .reset-btn > div[data-testid="stButton"] > button {
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.65rem !important;
        width: auto !important;
        height: auto !important;
        padding: 10px 28px !important;
        border: 2px solid #ff4e50 !important;
        background: #0d0d0d !important;
        color: #ff4e50 !important;
        letter-spacing: 2px !important;
        border-radius: 4px !important;
        display: block;
        margin: 0 auto !important;
    }

    .reset-btn > div[data-testid="stButton"] > button:hover {
        background: #ff4e5015 !important;
        box-shadow: 0 0 14px #ff4e5055 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    if "board" not in st.session_state:
        st.session_state.board = reset_board()
    if "current_player" not in st.session_state:
        st.session_state.current_player = 1       # 1 = X, -1 = O
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}

init_state()

# ── Helpers ───────────────────────────────────────────────────────────────────
SYMBOLS = {0: " ", 1: "X", -1: "O"}
PLAYER_NAMES = {1: "X", -1: "O"}

def handle_click(row, col):
    if st.session_state.game_over:
        return
    b = st.session_state.board
    if b[row, col] != 0:
        return
    make_move(b, row, col, st.session_state.current_player)

    winner = check_winner(b)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
        st.session_state.scores[winner] += 1
    elif is_draw(b):
        st.session_state.winner = "Draw"
        st.session_state.game_over = True
        st.session_state.scores["Draw"] += 1
    else:
        st.session_state.current_player *= -1

def do_reset():
    st.session_state.board = reset_board()
    st.session_state.current_player = 1
    st.session_state.game_over = False
    st.session_state.winner = None

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="game-title">TIC · TAC · TOE</div>', unsafe_allow_html=True)

# ── Scoreboard ────────────────────────────────────────────────────────────────
sc = st.session_state.scores
st.markdown(
    f"""
    <div class="score-row">
        <div class="score-card x">X<br><br>{sc['X']}</div>
        <div class="score-card d">DRAW<br><br>{sc['Draw']}</div>
        <div class="score-card o">O<br><br>{sc['O']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Status banner ─────────────────────────────────────────────────────────────
if st.session_state.game_over:
    w = st.session_state.winner
    if w == "Draw":
        cls, msg = "draw", "⚡ IT'S A DRAW ⚡"
    elif w == "X":
        cls, msg = "", "🏆 PLAYER X WINS!"
    else:
        cls, msg = "player-o", "🏆 PLAYER O WINS!"
else:
    p = PLAYER_NAMES[st.session_state.current_player]
    cls = "" if p == "X" else "player-o"
    msg = f"PLAYER {p}'S TURN"

st.markdown(f'<div class="status-banner {cls}">{msg}</div>', unsafe_allow_html=True)

# ── Board grid ────────────────────────────────────────────────────────────────
b = st.session_state.board

for r in range(3):
    cols = st.columns(3, gap="small")
    for c in range(3):
        val = b[r, c]
        symbol = SYMBOLS[val]
        cell_class = {1: "x-cell", -1: "o-cell", 0: ""}.get(val, "")
        disabled = (val != 0) or st.session_state.game_over

        with cols[c]:
            st.markdown(f'<div class="{cell_class}">', unsafe_allow_html=True)
            st.button(
                symbol if symbol.strip() else "·",
                key=f"cell_{r}_{c}",
                on_click=handle_click,
                args=(r, c),
                disabled=disabled,
            )
            st.markdown("</div>", unsafe_allow_html=True)

# ── Reset button ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
st.button("NEW GAME", on_click=do_reset, key="reset")
st.markdown("</div>", unsafe_allow_html=True)