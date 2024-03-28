from flask import jsonify
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from constants import SINGLE_GENERATION_TEMPLATE, SINGLE_GENERATION_HUMAN, MULTI_GENERATION_TEMPLATE, MULTI_GENERATION_HUMAN
from githubContent import GithubContent
from krokiClient import KrokiClient
from anthropic import BadRequestError

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage, SystemMessage

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
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", SINGLE_GENERATION_HUMAN)])
        chain = prompt | chat
        
        response = chain.invoke({"code": code})

        # model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=, convert_system_message_to_human=True)
        # response = model.invoke(
        #     [
        #         SystemMessage(content=system),
        #         HumanMessage(content=SINGLE_GENERATION_HUMAN(code)),
        #     ]
        # )

        print(response.content)
        return KrokiClient.getMermaidSVG(response.content)
    
    def multi_generation(repos):
        index = 1
        code = ""
        for repo in repos:
            tree = GithubContent.getGitHubTree(repo)
            code += GithubContent.getContentString(repo, tree, index)
            index += 1

        chat = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
        system = (MULTI_GENERATION_TEMPLATE)
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", MULTI_GENERATION_HUMAN)])
        chain = prompt | chat
        response = chain.invoke({"code": code})
        # print(response.content)
        return KrokiClient.getMermaidSVG(response.content)
    