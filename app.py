from flask import Flask, Response, request
import requests

app = Flask(__name__)
# Jouw Render URL (zonder trailing slash)
MY_PROXY_URL = "https://jouw-app.onrender.com" 
TARGET_URL = "https://js.puter.com/v2"

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/', defaults={'subpath': ''})
def proxy(subpath):
    url = f"{TARGET_URL}/{subpath}"
    
    # Haal de data op
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        params=request.args,
        allow_redirects=False
    )
    
    # Als het content is (JS of tekst), vervang dan de URL's
    content = resp.content
    if 'text/javascript' in resp.headers.get('Content-Type', '') or \
       'application/javascript' in resp.headers.get('Content-Type', ''):
        # Converteer naar tekst en vervang de originele URL door jouw proxy URL
        text_content = resp.text.replace(TARGET_URL, MY_PROXY_URL)
        content = text_content.encode('utf-8')

    headers = {key: value for (key, value) in resp.headers.items() 
               if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']}
    headers['Access-Control-Allow-Origin'] = '*'
    
    return Response(content, resp.status_code, headers)

if __name__ == '__main__':
    app.run()
