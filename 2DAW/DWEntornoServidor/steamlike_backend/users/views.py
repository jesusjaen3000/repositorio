import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login  # Importaciones nuevas
from .services import EmailService # Importación necesaria para el Ejercicio 5
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_json_request(request):
    try:
        body = request.body.decode("utf-8")
        if not body:
            return {}
        return json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}

@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    data = get_json_request(request)

    if not data:
        return JsonResponse({
            "error": "validation_error",
            "message": "Datos de entrada inválidos",
            "details": {"body": "El cuerpo de la petición no puede estar vacío"}
        }, status=400)

    errores = False
    errores_dict = {}

    username = data.get("username")
    password = data.get("password")
    email = data.get("email") 

    # --- Validaciones (Ejercicio 4) ---
    if username is None:
        errores = True
        errores_dict.update({"username": "Campo obligatorio"})
    elif not isinstance(username, str):
        errores = True
        errores_dict.update({"username": "Debe ser una cadena"})

    if password is None:
        errores = True
        errores_dict.update({"password": "Campo obligatorio"})
    elif not isinstance(password, str):
        errores = True
        errores_dict.update({"password": "Debe ser una cadena"})

    if email is None:
        errores = True
        errores_dict.update({"email": "Campo obligatorio"})
    elif not isinstance(email, str) or "@" not in email:
        errores = True
        errores_dict.update({"email": "Email inválido"})

    if isinstance(password, str) and len(password) < 8:
        errores = True
        errores_dict.update({"password": "La contraseña debe tener al menos 8 caracteres"})

    if isinstance(username, str) and User.objects.filter(username=username).exists():
        errores = True
        errores_dict.update({"username": "duplicate"})

    if errores:
        return JsonResponse({
            "error": "validation_error",
            "message": "Datos de entrada inválidos",
            "details": errores_dict
        }, status=400)

    # --- Crear usuario ---
    user = User.objects.create_user(username=username, password=password, email=email)

    # --- LOG Y ENVÍO AUTOMÁTICO (Ejercicio 3 y 5) ---
    # Registramos el intento de envío tras el registro exitoso
    logger.info(f"[ACTION: register_welcome_email] [USER: {user.username}] [DEST: {user.email}] Enviando bienvenida automática")

    # Llamada al servicio que ya devuelve éxito y código (gracias al Ejercicio 4 de resiliencia)
    success, status_code = EmailService.send_email(
        to=user.email,
        subject="Bienvenido a SteamLike",
        text=f"Hola {user.username}, gracias por registrarte."
    )

    if success:
        # Log de éxito
        logger.info(f"[ACTION: register_welcome_email] [USER: {user.username}] [RESULT: ok]")
    else:
        # Log de error (si falla Maileroo, el usuario se crea igual pero registramos el fallo del email)
        tipo_error = "error_503" if status_code == 503 else "error_502"
        logger.error(f"[ACTION: register_welcome_email] [USER: {user.username}] [RESULT: {tipo_error}] Status: {status_code}")

    # Respuesta oficial (Ejercicio 4: Incluye el email)
    return JsonResponse({
        "id": user.id, 
        "username": user.username, 
        "email": user.email
    }, status=201)
# --- NUEVAS VISTAS PARA EL EJERCICIO 3 ---

@require_http_methods(["POST"])
@csrf_exempt
def login_view(request):
    data = get_json_request(request)
    username = data.get("username")
    password = data.get("password")

    # Validación de tipos y presencia (400) 
    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse({
            "error": "validation_error",
            "message": "Datos de entrada inválidos"
        }, status=400)

    # Intentar autenticar al usuario
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Crea la sesión en el servidor
        return JsonResponse({
            "id": user.id,
            "username": user.username
        }, status=200)
    else:
        # MODIFICACIÓN PARA TESTS: El mensaje debe ser exactamente "Credenciales incorrectas" en el campo error
        return JsonResponse({
            "error": "Credenciales incorrectas",
            "message": "Credenciales incorrectas"
        }, status=401)

@require_http_methods(["GET"])
def me_view(request):
    # Comprobar si el usuario tiene una sesión activa
    if request.user.is_authenticated:
        return JsonResponse({
            "id": request.user.id,
            "username": request.user.username
        }, status=200)
    else:
        # MODIFICACIÓN PARA TESTS: El mensaje debe ser exactamente "No autenticado" en el campo error
        return JsonResponse({
            "error": "No autenticado",
            "message": "No autenticado"
        }, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def debug_email_test(request):
    data = get_json_request(request)
    to = data.get("to")
    subject = data.get("subject")
    text = data.get("text")

    # Obtenemos el nombre del usuario para el log (Ejercicio 3)
    u_name = request.user.username if request.user.is_authenticated else "anonymous"

    # Validación de campos
    if not all([to, subject, text]):
        return JsonResponse({"error": "validation_error"}, status=400)

    # --- LOG EJERCICIO 3: Intento de envío ---
    logger.info(f"[ACTION: send_email] [USER: {u_name}] [DEST: {to}] Intento de envío de prueba")

    # Llamada al servicio (Tu código original)
    success, status_code = EmailService.send_email(to, subject, text)
    
    if success:
        # --- LOG EJERCICIO 3: Envío OK ---
        logger.info(f"[ACTION: send_email] [USER: {u_name}] [DEST: {to}] [RESULT: ok]")
        return JsonResponse({"ok": True}, status=200)
    
    # --- LOG EJERCICIO 3: Fallo por respuesta o red (502/503) ---
    # Si el status_code es 0 suele ser error de red (503), si es otro, error de proveedor (502)
    tipo_error = "error_503" if status_code == 0 else "error_502"
    logger.error(f"[ACTION: send_email] [USER: {u_name}] [DEST: {to}] [RESULT: {tipo_error}] Status API: {status_code}")

    # Tu respuesta original
    return JsonResponse({"error": "email_failed"}, status=502)