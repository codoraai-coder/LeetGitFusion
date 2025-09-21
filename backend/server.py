from fastapi import FastAPI
from backend import leetcode_routes, github_routes

app = FastAPI(title="AI Agents Backend")

app.include_router(leetcode_routes.router, prefix="/leetcode", tags=["LeetCode"])
app.include_router(github_routes.router, prefix="/github", tags=["GitHub"])
