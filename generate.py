from flask import jsonify
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from constants import SINGLE_GENERATION_TEMPLATE, HUMAN
from githubContent import GithubContent
from krokiClient import KrokiClient

class Generator:
    def generateDiagram(repos):
        num_repos = len(repos)
        if (num_repos == 0):
            return jsonify({'error': 'No repositories provided.'}), 400
        elif (num_repos == 1):
            return Generator.single_generation(repos)
        else:
            return Generator.multi_generation(repos)
        
    def single_generation(repos):
        tree = GithubContent.getGitHubTree(repos[0])
        code = GithubContent.getContentString(repos[0], tree, 1)

        chat = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
        system = (SINGLE_GENERATION_TEMPLATE)
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", HUMAN)])
        chain = prompt | chat
        response = chain.invoke({"code": code})
        return KrokiClient.getMermaidSVG(response.content)
    
    def multi_generation(repos):
        index = 1
        code = ""
        for repo in repos:
            tree = GithubContent.getGitHubTree(repo)
            code += GithubContent.getContentString(repo, tree, index)
            index += 1

        return jsonify({'message': 'JSON processed successfully'}), 200

    