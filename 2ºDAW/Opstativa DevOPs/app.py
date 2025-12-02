//app.py
import os

mensaje = os.getenv("MENSAJE", "Hola desde Python optimizado!")
print(mensaje)
