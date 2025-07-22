import requests, json, os

TOOL_HISTORY_FILE = 'posted_tools.json'
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK_URL']

def fetch_tools():
    url = 'https://api.github.com/search/repositories?q=hacking+tools&sort=stars&order=desc&per_page=30'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers=headers)
    return r.json()['items']

def load_history():
    try:
        with open(TOOL_HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(TOOL_HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def post_to_discord(repo):
    embed = {
        "title": repo['name'],
        "description": repo['description'] or "No description provided.",
        "url": repo['html_url'],
        "fields": [
            {"name": "⭐ Stars", "value": str(repo['stargazers_count'])},
            {"name": "👨‍💻 Language", "value": str(repo['language'] or "Unknown")}
        ]
    }
    data = {"embeds": [embed]}
    requests.post(DISCORD_WEBHOOK, json=data)

def main():
    tools = fetch_tools()
    history = load_history()
    for tool in tools:
        if tool['html_url'] not in history:
            post_to_discord(tool)
            history.append(tool['html_url'])
            save_history(history)
            break
    else:
        print("No new tools found!")

main()
