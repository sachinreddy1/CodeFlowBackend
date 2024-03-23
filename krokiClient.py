from flask import jsonify, Response
import requests

class KrokiClient:
    def getMermaidSVG(data):
        url = "https://kroki.io/mermaid/svg"
        headers = {
            'Content-Type': 'text/plain',
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return Response(response.content, mimetype='image/svg+xml', headers={"Content-disposition": 'attachment; filename="diagram.svg"'})
        else:
            return jsonify({'error': 'Unable to fetch SVG.'}), 400