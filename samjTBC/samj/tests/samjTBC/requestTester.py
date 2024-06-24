import requests
import sys

def make_request(phone_number):
    # URL des Webservices
    url = "http://localhost:7000/restEndpoint/"
    
    # Parameter für die Anfrage
    params = {
        'number': phone_number
    }
    
    # Anfrage an den Webservice senden
    response = requests.get(url, params=params)
    
    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Antwort zurückgeben
        return response.text
    else:
        return f"Fehler: {response.status_code}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <phone_number>")
    else:
        phone_number = sys.argv[1]
        result = make_request(phone_number)
        print(result)
