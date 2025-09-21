def extract_deploy_links(repos):
    return [repo["homepage"] for repo in repos if repo.get("homepage")]

def count_commits(repos):
    total_commits = sum(repo.get("size", 0) for repo in repos)  # proxy if commit API not called
    return total_commits
