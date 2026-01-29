import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.contrib.auth.models import User
from library.models import LibraryEntry

def get_json_request(request):
    """
    Devuelve el cuerpo JSON del request como dict.
    Si el body está vacío o es inválido, devuelve {}.
    """
    try:
        body = request.body.decode("utf-8")
        if not body:
            return {}
        return json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}

@require_GET
def health(request):
    return JsonResponse({"status": "ok"})

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        data = get_json_request(request)
        username = data.get('username')
        password = data.get('password')

        # Validación de campos obligatorios, tipos y contenido
        if not username or not password or not isinstance(username, str) or not isinstance(password, str) or not username.strip():
            return JsonResponse({
                "error": "validation_error",
                "message": "Faltan campos obligatorios o el formato es incorrecto"
            }, status=400)

        # Validación longitud contraseña (mínimo 8)
        if len(password) < 8:
            return JsonResponse({
                "error": "validation_error",
                "message": "La contraseña debe tener al menos 8 caracteres"
            }, status=400)

        try:
            # Crear usuario (encripta la clave automáticamente)
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({
                "id": user.id,
                "username": user.username
            }, status=201)
        except IntegrityError:
            return JsonResponse({
                "error": "validation_error",
                "message": "El nombre de usuario ya está en uso"
            }, status=400)

@require_http_methods(["GET", "POST"])
@csrf_exempt
def add_library_entry(request):
    # 1. PROTECCIÓN: Autenticación
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized", "message": "No autenticado"}, status=401)
    
    if request.method == "POST":
        data = get_json_request(request)
        external_game_id = data.get("external_game_id")
        status = data.get("status")
        hours_played = data.get("hours_played", 0)
        
        errores_dict = {}

        # 2. VALIDACIÓN: Tipos y obligatoriedad
        if not external_game_id:
            errores_dict.update({"external_game_id": "Este campo es obligatorio"})
        
        if not isinstance(hours_played, int) or hours_played < 0:
            errores_dict.update({"hours_played": "Las horas deben ser un número entero positivo"})

        if status not in ["wishlist", "playing", "completed", "dropped"]:
            errores_dict.update({"status": "Estado no permitido"})

        if not errores_dict:
            try:
                # ASOCIACIÓN AUTOMÁTICA AL USUARIO
                entry = LibraryEntry.objects.create(
                    external_game_id=external_game_id,
                    status=status,
                    hours_played=hours_played,
                    user=request.user
                ) 
                return JsonResponse({
                    "id": entry.id, 
                    "external_game_id": entry.external_game_id,
                    "status": entry.status, 
                    "hours_played": entry.hours_played
                }, status=201)
            except IntegrityError:
                return JsonResponse({
                    "error": "duplicate_entry",
                    "message": "El juego ya existe en tu biblioteca",
                    "details": {"external_game_id": "duplicate"}
                }, status=400)
        else:
            return JsonResponse({
                "error": "validation_error",
                "message": "Datos de entrada inválidos",
                "details": errores_dict
            }, status=400)

    elif request.method == "GET":
        # PRIVACIDAD: Solo lo propio
        entries = LibraryEntry.objects.filter(user=request.user)
        response_entries = [
            {
                "id": e.id,
                "external_game_id": e.external_game_id,
                "status": e.status,
                "hours_played": e.hours_played
            } for e in entries
        ]
        return JsonResponse(response_entries, status=200, safe=False) 
    
    return JsonResponse({"error": "method_not_allowed", "message": "Método no permitido"}, status=405)

@require_http_methods(["GET", "PATCH"])
@csrf_exempt
def library_entry_detail(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized", "message": "No autenticado"}, status=401)

    try:
        # Filtro por ID y Usuario (Seguridad de propiedad)
        entry = LibraryEntry.objects.get(id=id, user=request.user)
    except LibraryEntry.DoesNotExist:
        return JsonResponse({
            "error": "not_found",
            "message": "La entrada solicitada no existe"
        }, status=404)

    if request.method == 'GET':
        return JsonResponse({
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        }, status=200)

    elif request.method == 'PATCH':
        data = get_json_request(request)
        if not data:
            return JsonResponse({
                "error": "validation_error",
                "message": "Cuerpo vacío",
                "details": {"body": "El cuerpo no puede estar vacío"}
            }, status=400)
        
        # Validar campos permitidos
        allowed_fields = {'status', 'hours_played'}
        if not any(field in data for field in allowed_fields):
             return JsonResponse({
                "error": "validation_error",
                "message": "Debe incluir al menos 'status' o 'hours_played'"
            }, status=400)

        errores_dict = {}
        if 'hours_played' in data:
            if not isinstance(data['hours_played'], int) or data['hours_played'] < 0:
                errores_dict.update({"hours_played": "Debe ser un entero positivo"})
        
        if 'status' in data:
            if data['status'] not in ["wishlist", "playing", "completed", "dropped"]:
                errores_dict.update({"status": "Estado no válido"})
        
        if errores_dict:
            return JsonResponse({
                "error": "validation_error",
                "message": "Datos inválidos",
                "details": errores_dict
            }, status=400)
        
        # Guardar cambios
        if 'status' in data: entry.status = data['status']
        if 'hours_played' in data: entry.hours_played = data['hours_played']
        entry.save()
        
        return JsonResponse({
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        }, status=200)

    return JsonResponse({"error": "method_not_allowed", "message": "Método no permitido"}, status=405)