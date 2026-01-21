import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
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


# Vista para añadir una entrada a la biblioteca
# Vista para añadir una entrada a la biblioteca
@require_http_methods(["GET", "POST"])
@csrf_exempt
def add_library_entry(request):
    if request.method == "POST":
        data= get_json_request(request)
        external_game_id = data.get("external_game_id")
        status = data.get("status")
        hours_played = data.get("hours_played", 0)
        errores_dict = {} # Diccionario para almacenar errores de validación

        #   Validación de datos
        errores = False  #Ausencia de errores
        if hours_played < 0:
            errores = True #Hayunerror
            errores_dict.update({"hours_played": "Las horas deben ser positivas"})

        if status not in ["wishlist", "playing", "completed", "dropped"]:
            errores = True
            errores_dict.update({"status": "Estado no permitido. Los valores permitidos son: wishlist, playing, completed, dropped"})
    
        #Los try except ayudan a capturar las excepciones, las excepciones son errores que pueden ocurrir en django
        #En este caso es una excepción de integridad (IntegrityError), esta sucede cuando se intenta duplicar un valor único en la base de datos
        #El external_game_id es único, por lo que si se intenta agregar un juego con un external_game_id que ya existe, se lanzará una excepción de integridad
        #El bloque try intenta crear la entrada en la base de datos, si tiene éxito, devuelve una respuesta JSON con los detalles de la entrada creada y un código de estado 201 (creado)
        #Si ocurre una excepción de integridad, se captura en el bloque except y se devuelve una respuesta JSON
        #No nos puede dar un error 500, los errores 500 los transformamos en 400 ya que estos errores el programador los tiene que especificar para que se capturen laa excepciones (errores)

        if errores == False:
            try:
                entry = LibraryEntry.objects.create(
                    external_game_id=external_game_id,
                    status=status,
                    hours_played=hours_played
                ) 
                return JsonResponse({"id": entry.id, "external_game_id": entry.external_game_id,"status":entry.status, "hours_played":entry.hours_played}, status=201)
            except IntegrityError:
                # El external_game_id ya existe en la biblioteca
                return JsonResponse({
                    "error": "duplicate_entry",
                    "message": "El juego ya existe en la biblioteca",
                    "details": {"external_game_id": "duplicate"}
                }, status=400)
        else:
            # Si hay errores de validación, devolver un error 400 con detalles
            return JsonResponse({
                "error": "validation_error" ,
                "message": "Datos de entrada inválidos",
                "details": errores_dict
                }, status=400)
    elif request.method == "GET":
        #Obtenemos todas lae entradas de la base de datos
        entries = LibraryEntry.objects.all()

        #Creamos una lista vacía para ir guardando las entradas de la biblioteca que luego enviaré como JSON
        response_entries = []
        
        for entry in entries:
            response_entries.append({
                "id": entry.id,
                "external_game_id":entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played
            })

        # Devolvemos la respuesta JSON con la lista de entradas
        return JsonResponse(response_entries, status=200, safe=False) #safe=False permite devolver listas como respuesta JSON
    else:
        return JsonResponse({"error": "method_not_allowed", 
        "message": "Método no permitido"}, status=405)


@require_http_methods(["GET", "PATCH"])
@csrf_exempt
def library_entry_detail(request, id):
    if request.method == 'GET':
        try:
            entry = LibraryEntry.objects.get(id=id)
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
        
        # Verificar que solo se acepten status y hours_played
        allowed_fields = {'status', 'hours_played'}
        for key in data:
            if key not in allowed_fields:
                return JsonResponse({
                    "error": "validation_error",
                    "message": "Datos de entrada inválidos",
                    "details": {key: "Campo no permitido"}
                }, status=400)
        
        # Verificar que al menos uno de los campos esté presente
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
