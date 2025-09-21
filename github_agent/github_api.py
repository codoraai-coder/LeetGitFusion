import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_github_profile(username):
    url = f"https://api.github.com/users/{username}"
    r = requests.get(url, headers=HEADERS)
    return r.json() if r.status_code == 200 else {}

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    r = requests.get(url, headers=HEADERS)
    return r.json() if r.status_code == 200 else []
