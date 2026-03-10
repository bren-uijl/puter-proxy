from flask import Flask, Response, request
import requests

app = Flask(__name__)
# Jouw specifieke URL
MY_PROXY_URL = "https://puter-proxy-czzt.onrender.com" 
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
    
    # Content-Type check
    content = resp.content
    is_js = 'text/javascript' in resp.headers.get('Content-Type', '') or \
            'application/javascript' in resp.headers.get('Content-Type', '')
            
    # URL's in de JS code vervangen zodat ze via jouw proxy blijven lopen
    if is_js:
        text_content = resp.text.replace(TARGET_URL, MY_PROXY_URL)
        content = text_content.encode('utf-8')

    # Headers opschonen
    headers = {key: value for (key, value) in resp.headers.items() 
               if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']}
    headers['Access-Control-Allow-Origin'] = '*'
    
    return Response(content, resp.status_code, headers)

if __name__ == '__main__':
    app.run()
