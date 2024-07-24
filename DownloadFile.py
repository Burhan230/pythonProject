import requests
import base64
import json


def fetch_github_file_content(owner, repo, file_path, access_token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_details = response.json()
        if file_details['encoding'] == 'base64':
            file_content = base64.b64decode(file_details['content']).decode('utf-8')
        else:
            file_content = file_details['content']
        return file_content, file_details['sha']
    else:
        raise Exception(f"Error fetching file: {response.status_code}, {response.text}")


def update_github_file_content(owner, repo, file_path, new_content, sha, access_token, commit_message):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {'Authorization': f'token {access_token}'}

    content_encoded = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

    data = {
        "message": commit_message,
        "content": content_encoded,
        "sha": sha
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error updating file: {response.status_code}, {response.text}")


# Example usage:
owner = "Burhan230"
repo = "pythonProject"
file_path = "app.py"
access_token = "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"  # Optional, if the repository is private or to avoid rate limits

try:
    # Step 1: Fetch the current content and SHA of the file
    current_content, sha = fetch_github_file_content(owner, repo, file_path, access_token)
    print("Current content fetched successfully.")

    # Save the current content to a local file
    with open("downloaded_file.py", "w") as file:
        file.write(current_content)
    print("File downloaded and saved locally.")

    # # Modify the content as needed
    # new_content = current_content + "\n\n# New Content\nThis is the added content."
    #
    # # Step 2: Update the content of the file
    # commit_message = "Update README.md with new content"
    # update_response = update_github_file_content(owner, repo, file_path, new_content, sha, access_token, commit_message)
    # print("File updated successfully.")
    # print(update_response)

except Exception as e:
    print(e)
