import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_user_with_openai(user_data):
    prompt = f"""
    Analyze this LeetCode user profile and return structured JSON.

    Input:
    {json.dumps(user_data, indent=2)}

    Output Format:
    {{
      "username": "...",
      "ranking": ...,
      "totalSolved": ...,
      "easySolved": ...,
      "mediumSolved": ...,
      "hardSolved": ...,
      "badges": [...],
      "plagiarismRisk": "...",
      "insights": "..."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI Agent for LeetCode profile analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Get raw content
    raw_content = response.choices[0].message.content.strip()
    print("Raw response from GPT:", raw_content)  # DEBUG
    
    # Sometimes GPT adds text before/after JSON; extract JSON only
    try:
        # Extract JSON object using regex
        json_text = re.search(r"\{.*\}", raw_content, re.DOTALL).group()
        return json.loads(json_text)
    except Exception as e:
        print("Failed to parse JSON:", e)
        return {
            "username": user_data.get("username", ""),
            "ranking": None,
            "totalSolved": 0,
            "easySolved": 0,
            "mediumSolved": 0,
            "hardSolved": 0,
            "badges": [],
            "plagiarismRisk": "Unknown",
            "insights": ""
        }
