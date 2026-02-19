import os
import requests
import json
import sys # Para forzar la salida

class EmailService:
    @staticmethod
    def send_email(to, subject, text):
        # Esto TIENE que salir en la terminal si la URL de Bruno es correcta
        print(">>> ¡CONTACTO CON EL SERVIDOR ESTABLECIDO! <<<", flush=True)
        
        api_key = os.getenv("MAILEROO_API_KEY")
        from_email = os.getenv("MAILEROO_DOMAIN_ID")
        
        payload = {
            "to": [{"address": to}],
            "subject": subject,
            "plain": text,
            "from": {"address": from_email} 
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        try:
            r = requests.post("https://smtp.maileroo.com/api/v2/emails", 
                             data=json.dumps(payload), 
                             headers=headers, 
                             timeout=15)
            print(f">>> MAILEROO RESPONDE: {r.status_code}", flush=True)
            return True, 200
        except Exception as e:
            print(f">>> ERROR CRÍTICO: {e}", flush=True)
            return False, 500