from flask import jsonify
from util import Util
from models import GitHubTreeResponse, GitHubBlobResponse
import requests
from dotenv import load_dotenv
import os

load_dotenv()
github_auth_token = os.getenv('GITHUB_AUTH_TOKEN')
github_tree_url = os.getenv('GITHUB_TREE_URL')
headers = {
    'Authorization': github_auth_token,
}

class GithubContent:
    def getGitHubTree(repo):
        formatted_url = github_tree_url.format(repo.owner, repo.repository, repo.branch)
        response = requests.get(formatted_url, headers=headers)
        if response.status_code == 200:
            github_tree_response = GitHubTreeResponse.from_json(response.text)
            tree = github_tree_response.tree
            return tree
        else:
            return jsonify({'error': 'Unable to fetch repository.'}), 400
        
    def getGitHubBlob(url):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            github_blob_response = GitHubBlobResponse.from_json(response.text)
            content = github_blob_response.content
            return content
        else:
            return jsonify({'error': 'Unable to fetch repository information.'}), 400
        
    def getContentString(repo, tree, i):
        ret = f"<repository index=\"{i}\">\n"

        ret += f"<repository_source>\n"
        ret += f"{repo.owner}/{repo.repository}/{repo.branch}\n"
        ret += f"</repository_source>\n"

        index = 1
        for i in tree:
            if (Util.isValidFileType(i.path) and i.url != None):
                blob = GithubContent.getGitHubBlob(i.url)
                if (blob):
                    ret += f"<document index=\"{index}\">\n"
                    ret += f"<source>\n"
                    ret += f"{i.path}\n"
                    ret += f"</source>\n"
                    ret += f"<document_content>\n"
                    ret += f"{Util.decodeBase64(blob)}\n"
                    ret += f"</document_content>\n"
                    ret += f"</document>\n"

                    index += 1

        ret += "</repository>\n"
        return ret