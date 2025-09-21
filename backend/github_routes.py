from fastapi import APIRouter
from github_agent.github_api import fetch_github_profile, fetch_repos
from github_agent.analyzer import analyze_github_user

router = APIRouter()

@router.get("/analyze/{username}")
def analyze(username: str):
    profile = fetch_github_profile(username)
    repos = fetch_repos(username)
    return {"analysis": analyze_github_user(profile, repos)}
