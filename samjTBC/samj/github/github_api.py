import requests
import os


# Replace with your GitHub token
token = os.environ['GITHUB_TOKEN_SAMJ']

# Replace with the repository owner and repository name
owner = 'SAMJ-CSDC26BB'
repo = 'SAMJ-Django-TBC'

# URL for creating an issue
url = f'https://api.github.com/repos/{owner}/{repo}/issues'

# Headers including the authorization token
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Data for the new issue
data = {
    'title': 'Issue title',
    'body': 'Description of the issue'
}

# Sending the request to create an issue
response = requests.post(url, headers=headers, json=data)

# Printing the response
if response.status_code == 201:
    print('Issue created successfully')
else:
    print('Failed to create issue')
    print('Response:', response.json())
