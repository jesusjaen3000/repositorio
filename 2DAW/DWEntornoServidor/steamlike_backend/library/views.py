import json
import requests # <--- IMPORTANTE: Asegúrate de añadir esta línea arriba
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.contrib.auth.models import User
from library.models import LibraryEntry
from django.contrib.auth import logout
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
    # 1. PROTECCIÓN: Autenticación (Ejercicio 5)
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "unauthorized", 
            "message": "No autenticado"
        }, status=401)
    
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

        if errores_dict:
            return JsonResponse({
                "error": "validation_error",
                "message": "Datos de entrada inválidos",
                "details": errores_dict
            }, status=400)

        # --- EJERCICIO 4: Validación Externa (Casos A, B y C) ---
        try:
            check_url = f"https://www.cheapshark.com/api/1.0/games?id={external_game_id}"
            check_resp = requests.get(check_url, timeout=5)
            
            # Caso B: Fallo externo por respuesta errónea (Status distinto de 200)
            if check_resp.status_code != 200:
                return JsonResponse({
                    "error": "external_service_error",
                    "message": "La API externa ha respondido con un error."
                }, status=502)

            # Caso C: Validación de existencia (ID no encontrado)
            if not check_resp.json():
                return JsonResponse({
                    "error": "invalid_external_game_id",
                    "message": "El juego indicado no existe en el catálogo externo.",
                    "details": {"external_game_id": "not_found"}
                }, status=400)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            # Caso A: Fallo externo por red o timeout
            return JsonResponse({
                "error": "external_service_unavailable",
                "message": "Servicio de validación externo no disponible o lento"
            }, status=503)
        except requests.exceptions.RequestException:
            # Error genérico de la librería requests
            return JsonResponse({
                "error": "external_service_unavailable",
                "message": "Error al conectar con el servicio externo"
            }, status=503)

        # 3. GUARDADO: Creación del registro asociado al usuario
        try:
            entry = LibraryEntry.objects.create(
                external_game_id=str(external_game_id), # Aseguramos que sea string
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

    elif request.method == "GET":
        # PRIVACIDAD: Solo devolvemos los juegos del usuario logueado
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
    
    return JsonResponse({"error": "method_not_allowed"}, status=405)

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

# === FUNCIONES UA7 CORREGIDAS SEGÚN PDF ===

@require_GET
def catalog_search(request):
    """
    Ejercicio 2: Buscador de catálogo externo
    Ejercicio 4: Manejo de errores de resiliencia (502, 503, 504, 400)
    """
    q = request.GET.get('q')
    
    # 1. VALIDACIÓN: Entrada obligatoria (Error 400)
    if not q or not q.strip():
        return JsonResponse({
            "error": "validation_error",
            "message": "El parámetro de búsqueda 'q' es obligatorio y no puede estar vacío."
        }, status=400)

    try:
        # 2. PETICIÓN: Con timeout de 5 segundos (Ejercicio 4 - Caso A)
        resp = requests.get(f"https://www.cheapshark.com/api/1.0/games?title={q}", timeout=5)
        
        # 3. RESILIENCIA: Error del proveedor (Ejercicio 4 - Caso B)
        if resp.status_code != 200:
            return JsonResponse({
                "error": "external_service_error",
                "message": "La API externa ha respondido con un error inesperado."
            }, status=502)
        
        data = resp.json()
        
        # 4. TRANSFORMACIÓN: (Ejercicio 2)
        # Normalizamos IDs a string y limitamos a 20 resultados
        results = [{
            "external_game_id": str(g['gameID']),
            "title": g['external'],
            "thumb": g['thumb']
        } for g in data[:20]]
        
        return JsonResponse(results, safe=False, status=200)
        
    except requests.exceptions.Timeout:
        # Manejo específico de agotamiento de tiempo (Ejercicio 4 - Caso A)
        return JsonResponse({
            "error": "external_service_timeout",
            "message": "El servicio externo ha tardado demasiado en responder (Timeout)."
        }, status=504)
        
    except requests.exceptions.RequestException:
        # Error genérico de red/conexión (Ejercicio 4)
        return JsonResponse({
            "error": "external_service_unavailable",
            "message": "No se ha podido establecer conexión con el catálogo externo."
        }, status=503)
    
@csrf_exempt
@require_http_methods(["POST"])
def catalog_resolve(request):
    """Ejercicio 3: Resolver IDs de catálogo con manejo de errores (Ejercicio 4)"""
    data = get_json_request(request)
    ids = data.get("external_game_ids")
    
    # 1. Validación de entrada (Error 400)
    if ids is None or not isinstance(ids, list) or len(ids) == 0:
        return JsonResponse({
            "error": "validation_error",
            "message": "Se requiere una lista 'external_game_ids' no vacía."
        }, status=400)

    resolved = []
    try:
        for gid in ids:
            # Añadimos timeout de 5 segundos (Ejercicio 4 - Caso A)
            resp = requests.get(f"https://www.cheapshark.com/api/1.0/games?id={gid}", timeout=5)
            
            # Caso B: Si la API responde con error (Error 502)
            if resp.status_code != 200:
                return JsonResponse({
                    "error": "external_service_error",
                    "message": f"Error al consultar el ID {gid} en CheapShark."
                }, status=502)

            g = resp.json()
            
            # Verificamos que el juego exista (si devuelve un dict vacío es que no existe)
            if g:
                resolved.append({
                    "external_game_id": str(gid),
                    "title": g.get('info', {}).get('title'),
                    "thumb": g.get('info', {}).get('thumb')
                })
        
        return JsonResponse(resolved, safe=False, status=200)

    except requests.exceptions.Timeout:
        # Manejo específico del Caso A (Ejercicio 4)
        return JsonResponse({
            "error": "external_service_timeout",
            "message": "La API externa ha tardado demasiado en responder durante la resolución de IDs."
        }, status=504)

    except requests.exceptions.RequestException:
        # Error genérico de red (Ejercicio 4)
        return JsonResponse({
            "error": "external_service_unavailable",
            "message": "El catálogo externo no está disponible. Inténtalo más tarde."
        }, status=503)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """
    Endpoint para cerrar la sesión del usuario.
    Limpia la sesión y la cookie de forma segura.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "unauthorized",
            "message": "No hay ninguna sesión activa para cerrar."
        }, status=401)

    logout(request)
    return JsonResponse({"message": "Sesión cerrada correctamente"}, status=200)
