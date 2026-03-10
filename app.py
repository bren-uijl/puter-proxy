from flask import Flask, Response, request
import requests

app = Flask(__name__)
MY_PROXY_URL = "https://puter-proxy-czzt.onrender.com"
TARGET_URL = "https://js.puter.com/v2"

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/', defaults={'subpath': ''})
def proxy(subpath):
    url = f"{TARGET_URL}/{subpath}"
    
    # Stuur het verzoek door
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key.lower() not in ['host', 'accept-encoding']},
        data=request.get_data(),
        params=request.args,
        allow_redirects=True
    )
    
    # We gebruiken resp.text om automatisch te decomprimeren
    content = resp.text
    
    # Vervang de URL's als het JavaScript is
    if 'javascript' in resp.headers.get('Content-Type', '').lower():
        content = content.replace(TARGET_URL, MY_PROXY_URL)

    # Bouw headers op, maar negeer de oude encoding/length headers
    headers = {key: value for (key, value) in resp.headers.items() 
               if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']}
    
    headers['Content-Type'] = resp.headers.get('Content-Type', 'application/javascript')
    headers['Access-Control-Allow-Origin'] = '*'
    
    return Response(content, resp.status_code, headers)

if __name__ == '__main__':
    app.run()
