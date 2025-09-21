import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from .utils import extract_deploy_links, count_commits

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_readme(repo):
    """
    Try to read README.md from local path or from repo dict if available.
    """
    # If repo has a local path to README
    if "local_path" in repo:
        readme_path = os.path.join(repo["local_path"], "README.md")
        if os.path.isfile(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                return f.read()
    # If repo dict has a 'readme' field
    if "readme" in repo:
        return repo["readme"]
    # Otherwise, not available
    return None

def analyze_github_user(profile, repos):
    # Calculate fields locally
    total_repos = len(repos)
    public_repos = sum(1 for repo in repos if not repo.get("private", False))
    private_repos = sum(1 for repo in repos if repo.get("private", False))
    total_commits = count_commits(repos)
    deployed_projects = extract_deploy_links(repos)
    collaborators = []
    readmes = {}
    for repo in repos:
        for collab in repo.get("collaborators", []):
            collaborators.append({"login": collab.get("login"), "id": collab.get("id")})
        # Add README content if available
        readme_content = read_readme(repo)
        if readme_content:
            readmes[repo.get("name", "unknown")] = readme_content

    # Use OpenAI only for insights and plagiarismRisk
    prompt = f"""
    Analyze this GitHub user and return JSON with only 'plagiarismRisk' and 'insights' fields.

    Profile:
    {json.dumps(profile, indent=2)}

    Repos:
    {json.dumps(repos[:3], indent=2)}

    Output Format:
    {{
      "plagiarismRisk": "...",
      "insights": "..."
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a GitHub profile analyzer."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content.strip()
    try:
        ai_result = json.loads(content)
    except:
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            try:
                ai_result = json.loads(match.group(0))
            except:
                ai_result = {"plagiarismRisk": "Unknown", "insights": "Could not parse AI response."}
        else:
            ai_result = {"plagiarismRisk": "Unknown", "insights": "Could not parse AI response."}

    # Combine all results
    return {
        "username": profile.get("login", ""),
        "totalRepos": total_repos,
        "publicRepos": public_repos,
        "privateRepos": private_repos,
        "totalCommits": total_commits,
        "collaborators": collaborators,
        "deployedProjects": deployed_projects,
        "readmes": readmes,
        "plagiarismRisk": ai_result.get("plagiarismRisk", ""),
        "insights": ai_result.get("insights", "")
    }

def analyze_multiple_users(profiles, repos_list):
    """
    Analyze multiple GitHub users.
    profiles: list of user profile dicts
    repos_list: list of list of repos, each corresponding to a user
    Returns: list of user analysis dicts
    """
    results = []
    for profile, repos in zip(profiles, repos_list):
        user_result = analyze_github_user(profile, repos)
        results.append(user_result)
    return results

def generate_leaderboard(user_analyses, key="totalCommits", top_n=10):
    """
    Generate a leaderboard sorted by a given key.
    user_analyses: list of user analysis dicts
    key: metric to sort by (e.g., 'totalCommits', 'totalRepos')
    top_n: number of top users to return
    Returns: sorted leaderboard list
    """
    for user in user_analyses:
        try:
            user[key] = int(user[key])
        except:
            user[key] = 0
    leaderboard = sorted(user_analyses, key=lambda x: x.get(key, 0), reverse=True)
    return leaderboard[:top_n]
