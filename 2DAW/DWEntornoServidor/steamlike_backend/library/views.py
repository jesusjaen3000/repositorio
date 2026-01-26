import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from library.models import LibraryEntry

# --- NUEVOS IMPORTS PARA EL EJERCICIO 2 ---
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
# ------------------------------------------

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

# --- NUEVA VISTA: EJERCICIO 2 (AÑADIDA) ---
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        data = get_json_request(request)
        username = data.get('username')
        password = data.get('password')

        # Validación de campos obligatorios y tipos
        if not username or not password or not isinstance(username, str) or not isinstance(password, str):
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

# --- TUS VISTAS ANTERIORES (SIN TOCAR NADA) ---

@require_http_methods(["GET", "POST"])
@csrf_exempt
def add_library_entry(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized", "message": "No autenticado"}, status=401)
    if request.method == "POST":
        data= get_json_request(request)
        external_game_id = data.get("external_game_id")
        status = data.get("status")
        hours_played = data.get("hours_played", 0)
        errores_dict = {} 

        errores = False  
        if hours_played < 0:
            errores = True 
            errores_dict.update({"hours_played": "Las horas deben ser positivas"})

        if status not in ["wishlist", "playing", "completed", "dropped"]:
            errores = True
            errores_dict.update({"status": "Estado no permitido. Los valores permitidos son: wishlist, playing, completed, dropped"})
    
        if errores == False:
            try:
                entry = LibraryEntry.objects.create(
                    external_game_id=external_game_id,
                    status=status,
                    hours_played=hours_played,
                    user=request.user
                ) 
                return JsonResponse({"id": entry.id, "external_game_id": entry.external_game_id,"status":entry.status, "hours_played":entry.hours_played}, status=201)
            except IntegrityError:
                return JsonResponse({
                    "error": "duplicate_entry",
                    "message": "El juego ya existe en la biblioteca",
                    "details": {"external_game_id": "duplicate"}
                }, status=400)
        else:
            return JsonResponse({
                "error": "validation_error" ,
                "message": "Datos de entrada inválidos",
                "details": errores_dict
                }, status=400)
    elif request.method == "GET":
        entries = LibraryEntry.objects.filter(user=request.user)
        response_entries = []
        for entry in entries:
            response_entries.append({
                "id": entry.id,
                "external_game_id":entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played
            })
        return JsonResponse(response_entries, status=200, safe=False) 
    else:
        return JsonResponse({"error": "method_not_allowed", "message": "Método no permitido"}, status=405)


@require_http_methods(["GET", "PATCH"])
@csrf_exempt
def library_entry_detail(request, id):
    if request.method == 'GET':
        try:
            entry = LibraryEntry.objects.get(id=id, user=request.user)
            response_entry = {
                "id": entry.id,
                "external_game_id": entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played
            }
            return JsonResponse(response_entry, status=200)
        except LibraryEntry.DoesNotExist:
            return JsonResponse({
                "error": "not_found",
                "message": "La entrada solicitada no existe"
            }, status=404)
    elif request.method == 'PATCH':
        data = get_json_request(request)
        if not data:
            return JsonResponse({
                "error": "validation_error",
                "message": "Datos de entrada inválidos",
                "details": {"body": "El cuerpo de la petición no puede estar vacío"}
            }, status=400)
        
        allowed_fields = {'status', 'hours_played'}
        for key in data:
            if key not in allowed_fields:
                return JsonResponse({
                    "error": "validation_error",
                    "message": "Datos de entrada inválidos",
                    "details": {key: "Campo no permitido"}
                }, status=400)
        
        if 'status' not in data and 'hours_played' not in data:
            return JsonResponse({
                "error": "validation_error",
                "message": "Datos de entrada inválidos",
                "details": {"body": "Debe incluir al menos 'status' o 'hours_played'"}
            }, status=400)
        
        errores_dict = {}
        errores = False
        
        if 'hours_played' in data:
            if not isinstance(data['hours_played'], int) or data['hours_played'] < 0:
                errores = True
                errores_dict.update({"hours_played": "Las horas deben ser un entero positivo"})
        
        if 'status' in data:
            if data['status'] not in ["wishlist", "playing", "completed", "dropped"]:
                errores = True
                errores_dict.update({"status": "Estado no permitido. Los valores permitidos son: wishlist, playing, completed, dropped"})
        
        if errores:
            return JsonResponse({
                "error": "validation_error",
                "message": "Datos de entrada inválidos",
                "details": errores_dict
            }, status=400)
        
        try:
            entry = LibraryEntry.objects.get(id=id)
            if 'status' in data:
                entry.status = data['status']
            if 'hours_played' in data:
                entry.hours_played = data['hours_played']
            entry.save()
            response_entry = {
                "id": entry.id,
                "external_game_id": entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played
            }
            return JsonResponse(response_entry, status=200)
        except LibraryEntry.DoesNotExist:
            return JsonResponse({
                "error": "not_found",
                "message": "La entrada solicitada no existe"
            }, status=404)
    else:
        return JsonResponse({
            "error": "method_not_allowed",
            "message": "Método no permitido"
        }, status=405)