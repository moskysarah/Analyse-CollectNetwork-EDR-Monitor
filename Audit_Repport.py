# audit_reporter.py (SecOps)
import json
import os

def generate_report():
    if os.path.exists("ad_audit_report.json"):
        with open("ad_audit_report.json", "r", encoding="utf-8") as f:
            report_data = json.load(f)
            
        print("=========================================")
        print(f"RAPPORT D'AUDIT AD - {report_data['ScanTime']}")
        print("=========================================")
        count = report_data['PasswordNeverExpiresCount']
        print(f"[-] Comptes avec mot de passe persistant : {count}")
        
        if count > 0:
            print("[CRITIQUE] Risque élevé de persistance en cas de vol de hash (Pass-the-Hash).")
            print("Action recommandée : Exécuter le module de durcissement.")
            # Appel du correcteur C++ pour durcir les politiques de sécurité locales si nécessaire
            
generate_report()