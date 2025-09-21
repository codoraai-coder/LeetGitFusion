import requests

LEETCODE_URL = "https://leetcode.com/graphql"

def fetch_leetcode_data(username: str):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        profile {
          ranking
          reputation
        }
        badges {
          displayName
        }
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    response = requests.post(LEETCODE_URL, json={"query": query, "variables": {"username": username}})
    if response.status_code == 200:
        return response.json()["data"]["matchedUser"]
    else:
        raise Exception(f"LeetCode API error: {response.text}")
