import requests
import base64


def fetch_github_file_content(owner, repo, file_path, access_token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {}
    if access_token:
        headers['Authorization'] = f'token {access_token}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_details = response.json()
        if file_details['encoding'] == 'base64':
            file_content = base64.b64decode(file_details['content']).decode('utf-8')
        else:
            file_content = file_details['content']
        return file_content
    else:
        return f"Error: {response.status_code}, {response.text}"


# Example usage:
owner = "Burhan230"
repo = "pythonProject"
file_path = "app.py"
access_token = "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"  # Optional, if the repository is private or to avoid rate limits

file_content = fetch_github_file_content(owner, repo, file_path, access_token)
print(file_content)
