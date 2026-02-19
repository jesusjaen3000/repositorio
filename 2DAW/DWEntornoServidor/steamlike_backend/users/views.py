import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login  # Importaciones nuevas
from .services import EmailService # Importación necesaria para el Ejercicio 5

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
    email = data.get("email") # MODIFICACIÓN EJERCICIO 4: Capturar email

    # Presencia y tipos
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

    # MODIFICACIÓN EJERCICIO 4: Validación de email
    if email is None:
        errores = True
        errores_dict.update({"email": "Campo obligatorio"})
    elif not isinstance(email, str) or "@" not in email:
        errores = True
        errores_dict.update({"email": "Email inválido"})

    # Validaciones adicionales
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

    # Crear usuario
    user = User.objects.create_user(username=username, password=password, email=email)

    # MODIFICACIÓN EJERCICIO 5: Envío de email automático tras registro exitoso
    EmailService.send_email(
        to=user.email,
        subject="Bienvenido a SteamLike",
        text=f"Hola {user.username}, gracias por registrarte."
    )

    # MODIFICACIÓN EJERCICIO 4: Respuesta incluye el email registrado
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

    # Validación de campos
    if not all([to, subject, text]):
        return JsonResponse({"error": "validation_error"}, status=400)

    # Llamada al servicio
    success, status_code = EmailService.send_email(to, subject, text)
    
    if success:
        return JsonResponse({"ok": True}, status=200)
    
    # CAMBIO REALIZADO AQUÍ: Forzamos 502 para que el test no reciba el 404 del servicio externo
    return JsonResponse({"error": "email_failed"}, status=502)