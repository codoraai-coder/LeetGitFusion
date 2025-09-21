from .leetcode_api import fetch_leetcode_data
from .agent import analyze_user_with_openai

def build_leetcode_leaderboard(usernames):
    board = []
    for u in usernames:
        raw = fetch_leetcode_data(u)
        analyzed = analyze_user_with_openai(raw)
        board.append(analyzed)

    board_sorted = sorted(board, key=lambda x: x["totalSolved"], reverse=True)
    return board_sorted
