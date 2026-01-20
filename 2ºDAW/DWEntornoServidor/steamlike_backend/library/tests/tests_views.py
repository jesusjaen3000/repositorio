from django.test import TestCase
from library.models import LibraryEntry
import json

class LibraryEntryExternalIdLengthTests(TestCase):
    def test_health(self):
        # Precondiciones

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/health/")

        # Comprobaciones
        # Comprobar el código HTTP que devuelve una vista
        self.assertEqual(response.status_code, 200)
        # Comprobar el contenido de la respuesta
        self.assertEqual(response.json(), {"status": "ok"})
        # Verifica que una clave existe dentro del JSON de la respuesta.
        self.assertIn("status", response.json())
        # Comprueba el valor concreto devuelto por la vista.
        self.assertEqual(response.json()["status"], "ok")
        # Asegura que la respuesta no contiene información que no debería aparecer.
        self.assertNotIn("paco", response.json())

class LibraryEntriesAPITests(TestCase):
    def setUp(self):
        # Crear al menos 2 entradas
        self.entry1 = LibraryEntry.objects.create(
            external_game_id="game1",
            status="playing",
            hours_played=10
        )
        self.entry2 = LibraryEntry.objects.create(
            external_game_id="game2",
            status="completed",
            hours_played=20
        )

    def test_list_entries(self):
        response = self.client.get("/api/library/entries/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        for entry in data:
            self.assertIn("id", entry)
            self.assertIn("external_game_id", entry)
            self.assertIn("status", entry)
            self.assertIn("hours_played", entry)
            # Asegurar que no hay campos extra
            self.assertEqual(len(entry), 4)

    def test_detail_existing_entry(self):
        response = self.client.get(f"/api/library/entries/{self.entry1.id}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.entry1.id)
        self.assertEqual(data["external_game_id"], "game1")
        self.assertEqual(data["status"], "playing")
        self.assertEqual(data["hours_played"], 10)
        # Asegurar que no hay campos extra
        self.assertEqual(len(data), 4)

    def test_detail_non_existing_entry(self):
        response = self.client.get("/api/library/entries/999/")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data, {
            "error": "not_found",
            "message": "La entrada solicitada no existe"
        })