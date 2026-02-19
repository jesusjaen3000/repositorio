import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse # Si usas nombres de ruta de Django

class LibraryEntryExternalIdLengthTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = '/api/register/'
        
        # MODIFICACIÓN: Creamos el usuario pep0 para que los tests de login funcionen
        # Usamos get_or_create para que sea más limpio
        self.user_pep0, created = User.objects.get_or_create(
            username="pep0",
            defaults={
                "email": "pep0@test.com"
            }
        )
        if created:
            self.user_pep0.set_password("12345678")
            self.user_pep0.save()
            
    def test_health(self):
        pass

    # --- NUEVOS TESTS DE REGISTRO ---

    def test_registro_valido_201(self):
        """Caso válido (201) y respuesta con id y username (sin contraseña)"""
        payload = {
            "username": "usuario_nuevo",
            "password": "PasswordSegura123",
            "email": "test@example.com"
        }
        response = self.client.post(
            self.url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertNotIn('password', data) # Verificamos que no se filtre la contraseña

    def test_registro_invalidos_400(self):
        """Casos no válidos (400): JSON vacío, faltan campos, contraseña corta"""
        casos = [
            ({}, "JSON vacío"),
            ({"username": "solo_user"}, "Falta contraseña"),
            ({"username": "user", "password": "12"}, "Contraseña corta"),
        ]

        for payload, descripcion in casos:
            with self.subTest(msg=descripcion):
                response = self.client.post(
                    self.url, 
                    data=json.dumps(payload), 
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, 400)

    def test_registro_username_repetido_400(self):
        """Caso no válido: username repetido"""
        # 1. Registramos un usuario primero
        payload = {"username": "pepe", "password": "Password123", "email": "pepe@test.com"}
        self.client.post(self.url, data=json.dumps(payload), content_type='application/json')

        # 2. Intentamos registrar el mismo username
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
    def test_login_valido_200(self):
        """Caso válido (200) con credenciales correctas"""
        # Primero aseguramos que el usuario existe
        user_data = {"username": "test_login", "password": "Password123", "email": "test_login@test.com"}
        self.client.post('/api/register/', data=json.dumps(user_data), content_type='application/json')

        # Intentamos el login
        response = self.client.post(
            '/api/auth/login/', 
            data=json.dumps(user_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

# --- TESTS EJERCICIO 2: LOGIN ---

    def test_login_valido_200_duplicate(self): # Renombrado ligeramente para evitar conflicto de nombres en la clase
        """Caso válido (200)"""
        # Usamos pep0 que ya vimos en tu Bruno que existe
        payload = {"username": "pep0", "password": "12345678"}
        response = self.client.post(
            '/api/auth/login/', 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_login_credenciales_incorrectas_401(self):
        """Caso no válido: credenciales incorrectas (401)"""
        payload = {"username": "pep0", "password": "password_mal"}
        response = self.client.post(
            '/api/auth/login/', 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        # Verifica que el mensaje sea exactamente el que pide el ejercicio
        self.assertEqual(response.json().get('error'), "Credenciales incorrectas")

    def test_login_error_validacion_400(self):
        """Caso no válido: validación (400)"""
        payload = {"username": "pep0"} # Falta el campo password
        response = self.client.post(
            '/api/auth/login/', 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

# --- TESTS EJERCICIO 3: PERFIL (ME) ---

    def test_me_sin_autenticar_401(self):
        """Caso no válido: Acceso sin sesión (401)"""
        response = self.client.get('/api/users/me/')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('error'), "No autenticado")

    def test_me_tras_login_200(self):
        """Caso válido: Acceso con sesión activa (200)"""
        # 1. Forzamos el login del usuario pep0 creado en setUp
        self.client.force_login(self.user_pep0)

        # 2. Ahora pedimos el perfil
        response = self.client.get('/api/users/me/')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertEqual(data['username'], 'pep0')

# --- NUEVOS TESTS EJERCICIO 2: DEBUG EMAIL ---

    def test_debug_email_valido_200(self):
        """Caso válido: Envío de email de prueba (Ejercicio 2)"""
        payload = {
            "to": "test@maileroo.com",
            "subject": "Test UA8",
            "text": "Hola mundo"
        }
        # Nota: Asegúrate de tener esta ruta configurada en urls.py
        response = self.client.post(
            '/api/debug/email/test/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Puede ser 200 si Maileroo responde OK o 502/503 si falla el servicio externo
        self.assertIn(response.status_code, [200, 502, 503])

    def test_debug_email_valido_200(self):
        """Caso válido: Envío de email de prueba (Ejercicio 2)"""
        from django.urls import reverse
        payload = {
            "to": "test@maileroo.com",
            "subject": "Test UA8",
            "text": "Hola mundo"
        }
        
        # Esto busca la ruta por el nombre que pusimos en el Paso 1
        try:
            url = reverse('debug_email_test')
        except:
            url = '/api/debug/email/test/'

        response = self.client.post(
            url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        # Verificamos que no sea 404
        self.assertNotEqual(response.status_code, 404, "Sigue dando 404. Revisa que hayas guardado urls.py")
        self.assertIn(response.status_code, [200, 502, 503])