import logging
import os

import requests

from samjTBC.logger import CustomFormatter


class GitHubAPI:
    # Create a logger instance
    logger = logging.getLogger(__name__)

    # Define log file path
    log_file_path = 'samjTBC/logs/support.log'

    # Check if the directory exists, if not, create it
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a file handler
    handler = logging.FileHandler(log_file_path)

    # Set the formatter for the handler
    handler.setFormatter(CustomFormatter())

    # Add the handler to the logger
    logger.addHandler(handler)

    def __init__(self):
        self.gh_token = os.getenv('GITHUB_TOKEN_SAMJ')
        self.owner = 'SAMJ-CSDC26BB'
        self.repo = 'SAMJ-Django-TBC'
        self.url = f'https://api.github.com/repos/{self.owner}/{self.repo}'

    def get_github_token(self):
        return self.gh_token

    def create_github_issue(self, title, body=None, labels=None):
        self.url = f'{self.url}/issues'
        data = {'title': {title}}
        headers = {
            'Authorization': f'token {self.gh_token}',
            'Accept': 'application/vnd.github_api.v3+json'
        }
        if body:
            data['body'] = body
        if labels:
            if isinstance(labels, str):
                labels = [labels]  # ensure labels is a list
            data['labels'] = labels

        self.logger.info('Sending request to GitHub API')
        response = requests.post(self.url, headers=headers, json=data)
        if response.status_code == 201:
            self.logger.info('Issue created successfully:%s', response.text)
        else:
            self.logger.error('Failed to create issue: %s', response.text)

        return response

    def list_github_issues(self, labels=None, state='open'):
        self.url = f'{self.url}/issues'
        query = {}
        headers = {
            'Authorization': f'token {self.gh_token}',
            'Accept': 'application/vnd.github_api.v3+json'
        }
        if labels:
            if isinstance(labels, str):
                labels = [labels]
            query = {
                'labels': labels
            }
        if state:
            query['state'] = state

        self.logger.info('Sending GET request to GitHub API')
        response = requests.get(self.url, headers=headers, params=query)
        if response.status_code == 201 or response.status_code == 200:
            self.logger.info(f'Github Issues listed successfully, {response.status_code}: {response.text}')
        else:
            self.logger.error(f'Failed to list github issues. {response.status_code}: {response.text}')

        return response.json()  # Extract JSON content from the response
