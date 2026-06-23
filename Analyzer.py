# analyzer.py
import json
import os
import time
import subprocess

def analyze_logs():
    print("[*] Analyse des logs en cours...")
    
    # 1. Lire la télémétrie réseau de PowerShell
    if os.path.exists("network_log.json"):
        with open("network_log.json", "r", encoding="utf-8") as f:
            try:
                network_data = json.load(f)
                # Exemple de règle : Alerte si connexion sur un port sensible (ex: 4444 - souvent utilisé par Metasploit)
                for conn in network_data:
                    if conn.get("RemotePort") == 4444:
                        print(f"[ALERT] Connexion suspecte détectée sur le port 4444 par le PID {conn.get('OwningProcess')}!")
                        trigger_remediation(conn.get("RemoteAddress"))
            except json.JSONDecodeError:
                pass

def trigger_remediation(ip):
    print(f"[!] Lancement de la réponse automatique contre l'IP : {ip}")
    # Appeler le script PowerShell de remédiation
    subprocess.run(["powershell.exe", "-Command", f".\\Network_Collector.ps1; Block-AttackersIP -IPAddress '{ip}'"])

if __name__ == "__main__":
    while True:
        analyze_logs()
        time.sleep(5)