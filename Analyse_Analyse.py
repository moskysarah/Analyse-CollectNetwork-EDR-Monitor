# siem_analyzer.py (Blue Team / SOC)
from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/siem-alert', methods=['POST'])
def alert():
    alert_data = request.json
    print(f"\n[🚨 ALERTE SOC - {datetime.datetime.now()}]")
    print(f"Événement critique détecté sur l'AD ! ID: {alert_data.get('EventID')}")
    print(f"Détails : {alert_data.get('Details')}")
    
    # Logique d'escalade : Si l'événement est critique, on pourrait déclencher un script PowerShell de remédiation
    return "Alerte traitée", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)