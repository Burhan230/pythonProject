import requests
import base64
import json


def fetch_github_file_sha(owner, repo, file_path, access_token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_details = response.json()
        return file_details['sha']
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"Error fetching file SHA: {response.status_code}, {response.text}")


def commit_file_to_github(owner, repo, file_path, local_file_path, access_token, commit_message):
    with open(local_file_path, 'r') as file:
        content = file.read()

    sha = fetch_github_file_sha(owner, repo, file_path, access_token)

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {'Authorization': f'token {access_token}'}

    content_encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    data = {
        "message": commit_message,
        "content": content_encoded,
        "sha": sha
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error committing file: {response.status_code}, {response.text}")


# Example usage:
owner = "Burhan230"
repo = "pythonProject"
file_path = "app.py"
access_token = "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"  # Optional, if the repository is private or to avoid rate limits
local_file_path = "C:/Users/burha/PycharmProjects/Helloworld/pythonProject/downloaded_file.py"
commit_message = "Add new content from local file"

try:
    commit_response = commit_file_to_github(owner, repo, file_path, local_file_path, access_token, commit_message)
    print("File committed successfully.")
    print(commit_response)
except Exception as e:
    print(e)
