from leetcode_agent.leaderboard_utils import build_leetcode_leaderboard
from github_agent.github_api import fetch_github_profile, fetch_repos
from github_agent.analyzer import analyze_github_user

def build_multi_user_leaderboard(le_usernames, gh_usernames):
    # LeetCode leaderboard
    le_board = build_leetcode_leaderboard(le_usernames) if le_usernames else []
    
    # GitHub leaderboard
    gh_board = []
    for u in gh_usernames:
        profile = fetch_github_profile(u)
        repos = fetch_repos(u)
        gh_board.append(analyze_github_user(profile, repos))
    
    gh_board_sorted = sorted(gh_board, key=lambda x: x.get("totalCommits", 0), reverse=True)
    for idx, user in enumerate(gh_board_sorted, start=1):
        user["rank"] = idx
    
    # Merge users for combined leaderboard
    combined = []
    usernames = set([u["username"] for u in le_board] + [u["username"] for u in gh_board_sorted])
    for u in usernames:
        le_data = next((x for x in le_board if x["username"] == u), {})
        gh_data = next((x for x in gh_board_sorted if x["username"] == u), {})
        combined.append({
            "username": u,
            "leetcode": le_data,
            "github": gh_data,
            "total_score": le_data.get("totalSolved",0) + gh_data.get("totalCommits",0)
        })
    
    combined_sorted = sorted(combined, key=lambda x: x["total_score"], reverse=True)
    for idx, user in enumerate(combined_sorted, start=1):
        user["rank"] = idx
    
    return combined_sorted
