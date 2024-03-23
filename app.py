import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import RepositoryInfo
from typing import List
from generate import Generator
from dotenv import load_dotenv

load_dotenv()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

app = Flask(__name__)
CORS(app)

@app.route('/v1/generate', methods=['POST'])
def generate():
    if not request.json:
        return jsonify({'error': 'Request body must be JSON'}), 400

    data = request.json

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        return jsonify({'error': 'Invalid JSON format'}), 400

    repos: List[RepositoryInfo] = [RepositoryInfo(**item) for item in data]
    return Generator.generateDiagram(repos)

if __name__ == "__main__":
    app.run(debug=True)