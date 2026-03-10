from flask import Flask, Response, request
import requests

app = Flask(__name__)

# CONFIGURATIE
MY_PROXY_URL = "https://puter-proxy-czzt.onrender.com"
JS_TARGET = "https://js.puter.com/v2"
SITE_TARGET = "https://puter.com"

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

@app.route('/<path:subpath>', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/', defaults={'subpath': ''})
def proxy(subpath):
    if request.method == 'OPTIONS':
        return Response(status=200)

    # Bepaal welk domein we moeten targeten. 
    # Als het verzoek om de inlogpagina of popups gaat, gebruiken we SITE_TARGET.
    if subpath.startswith('login') or 'request_auth' in request.args:
        url = f"{SITE_TARGET}/{subpath}"
    else:
        # Standaard gaan we naar de JS v2 bibliotheek
        url = f"{JS_TARGET}/{subpath}"
        if not subpath:
            url = JS_TARGET + "/"

    # Verwijder Accept-Encoding om compressie-fouten (wartaal) te voorkomen
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding']}

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            timeout=15,
            allow_redirects=True
        )

        # Voor tekstgebaseerde bestanden (HTML/JS) passen we de URL's aan
        content_type = resp.headers.get('Content-Type', '').lower()
        if any(t in content_type for t in ['javascript', 'html', 'json']):
            content = resp.text
            # Vervang alle bekende Puter domeinen door jouw proxy
            content = content.replace("https://js.puter.com/v2", MY_PROXY_URL)
            content = content.replace("https://puter.com", MY_PROXY_URL)
            return Response(content, resp.status_code, {'Content-Type': content_type})
        
        # Voor andere bestanden (zoals afbeeldingen/icoontjes) sturen we de ruwe bytes door
        return Response(resp.content, resp.status_code, {'Content-Type': content_type})

    except Exception as e:
        return Response(f"Proxy Error: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
