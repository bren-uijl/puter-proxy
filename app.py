from flask import Flask, Response, request
import requests

app = Flask(__name__)

# De bron-URL van Puter
PUTER_JS_URL = "https://js.puter.com/v2/"

@app.route('/')
def proxy_script():
    # 1. Haal de code op van Puter
    response = requests.get(PUTER_JS_URL)
    
    # 2. Maak een nieuw antwoord met de juiste "Content-Type" header
    # Dit zorgt ervoor dat de browser begrijpt dat het om JS gaat
    proxy_response = Response(
        response.content,
        status=response.status_code,
        headers={'Content-Type': 'application/javascript'}
    )
    
    # 3. Voeg CORS toe zodat jouw app vanaf elke website mag worden ingeladen
    proxy_response.headers['Access-Control-Allow-Origin'] = '*'
    
    return proxy_response

if __name__ == '__main__':
    app.run()
