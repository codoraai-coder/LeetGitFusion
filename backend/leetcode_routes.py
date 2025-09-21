from fastapi import APIRouter
from leetcode_agent.leaderboard_utils import build_leetcode_leaderboard

router = APIRouter()

@router.get("/leaderboard")
def leaderboard(usernames: str):
    users = [u.strip() for u in usernames.split(",")]
    return {"leaderboard": build_leetcode_leaderboard(users)}
