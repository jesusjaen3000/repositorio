import json
from library.models import LibraryEntry
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# --- FUNCIONES AUXILIARES (REFACTORIZACIÓN EJERCICIO 3) ---

def get_json_request(request):
    try:
        return json.loads(request.body.decode("utf-8")) if request.body else {}
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}

def json_res(data, status_code=200):
    """Simplifica la creación de respuestas JsonResponse."""
    return JsonResponse(data, status=status_code)

def error_res(error_type, message="", details=None, status_code=400):
    """Estandariza los errores para no repetir diccionarios."""
    payload = {"error": error_type}
    if message: payload["message"] = message
    if details: payload["details"] = details
    return json_res(payload, status_code)

# --- VISTAS ---

@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    data = get_json_request(request)
    if not data:
        return error_res("validation_error", "Cuerpo vacío", {"body": "No puede estar vacío"})

    u, p = data.get("username"), data.get("password")
    errs = {}

    if not isinstance(u, str): errs["username"] = "Obligatorio y cadena"
    if not isinstance(p, str) or len(p) < 8: errs["password"] = "Obligatorio y mín. 8 caracteres"
    if not errs and User.objects.filter(username=u).exists(): errs["username"] = "duplicate"

    if errs:
        return error_res("validation_error", "Datos inválidos", errs)

    user = User.objects.create_user(username=u, password=p)
    return json_res({"id": user.id, "username": user.username}, 201)

@require_http_methods(["POST"])
@csrf_exempt
def login_view(request):
    data = get_json_request(request)
    u, p = data.get("username"), data.get("password")

    if not isinstance(u, str) or not isinstance(p, str):
        return error_res("validation_error", "Datos inválidos")

    user = authenticate(request, username=u, password=p)
    if user:
        login(request, user)
        return json_res({"id": user.id, "username": user.username})
    
    return error_res("unauthorized", "Credenciales incorrectas", status_code=401)

@require_http_methods(["GET"])
def me_view(request):
    if not request.user.is_authenticated:
        return error_res("unauthorized", "No autenticado", status_code=401)
    
    return json_res({"id": request.user.id, "username": request.user.username})

@require_http_methods(["POST"])
@csrf_exempt
def change_password(request):
    if not request.user.is_authenticated:
        return error_res("unauthorized", status_code=401)

    data = get_json_request(request)
    curr, new = data.get("current_password"), data.get("new_password")

    # Validación según requisitos Ejercicio 2 [cite: 48, 49]
    if not curr or not new or len(new) < 8 or not request.user.check_password(curr):
        return error_res("validation_error")

    request.user.set_password(new)
    request.user.save()
    return json_res({"ok": True})

# --- EJERCICIO 4 y 6: Actualización completa (PUT) (PATCH) ---
@require_http_methods(["PUT", "PATCH"])
@csrf_exempt
def update_library_entry(request, entry_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized"}, status=401)

    data = get_json_request(request)

    # Si es PUT, obligamos a enviar todo (Ejercicio 4)
    if request.method == "PUT":
        required_fields = ["external_game_id", "status", "hours_played"]
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": "validation_error"}, status=400)

    try:
        entry = LibraryEntry.objects.get(id=entry_id, user=request.user)
        
        # Lógica de PATCH (Ejercicio 5): actualiza solo lo que venga en el JSON
        if "external_game_id" in data:
            entry.external_game_id = data["external_game_id"]
        if "status" in data:
            entry.status = data["status"]
        if "hours_played" in data:
            entry.hours_played = data["hours_played"]
            
        entry.save()

        return JsonResponse({
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        }, status=200)

    except LibraryEntry.DoesNotExist:
        return JsonResponse({"error": "not_found"}, status=404)

# --- EJERCICIO 6: Logout ---
@require_http_methods(["POST"])
@csrf_exempt
def logout_view(request):
    # El backend debe cerrar la sesión [cite: 128]
    if request.user.is_authenticated:
        logout(request) [cite: 138]
    
    # La respuesta es la misma tanto si estaba autenticado como si no [cite: 139]
    # Código 204 con body vacío [cite: 142, 143]
    return JsonResponse({}, status=204)

# --- EJERCICIO 7: Borrado de cuenta ---
@require_http_methods(["DELETE"])
@csrf_exempt
def delete_account(request):
    # El usuario debe estar autenticado [cite: 154]
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized"}, status=401) [cite: 165]

    user = request.user
    # Al borrar la cuenta, se borran sus entradas de biblioteca (por CASCADE en el modelo) [cite: 157]
    user.delete()
    
    return JsonResponse({}, status=204) [cite: 163]