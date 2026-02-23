import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email(to, subject, text):
        api_key = "a0a8621916188433006076433647ba766bb49843b6334ca03afd518f441c1dec"
        from_email = "test@d461399e50cd3a07.maileroo.org"
        
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
            # 1. Bajamos el timeout a 5 o 10 para ser más realistas (Ejercicio 4)
            r = requests.post(
                "https://smtp.maileroo.com/api/v2/emails", 
                data=json.dumps(payload), 
                headers=headers, 
                timeout=5 
            )

            # 2. Caso B: El proveedor responde pero algo va mal (Token caducado, etc)
            if r.status_code != 200:
                return False, 502
            
            return True, 200

        # 3. Caso A: Errores de red o el servidor de Maileroo tarda demasiado
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return False, 503
        
        # Otros errores de ejecución
        except Exception as e:
            return False, 500