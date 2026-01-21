from django.test import TestCase

from library.models import LibraryEntry

class DemoTest(TestCase):
    def test_demo(self):
        # Comprueba que dos valores son exactamente iguales.
        self.assertEqual(4, 2+2)
        # Comprueba si una condición se cumple o no.
        self.assertTrue(4 == 4)
        self.assertFalse(5 == 4)
        # Permiten distinguir entre None y otros valores como cadenas vacías o ceros.
        self.assertIsNone(None)
        # Comprueba que una acción provoca un error concreto.
        with self.assertRaises(ZeroDivisionError):
            # Codigo que lanza la excepcion
            4/0

class LibraryEntryExternalIdLengthTests(TestCase):
    def test_external_id_length_counts_regular_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_empty_string_as_zero(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 0)

    def test_external_id_length_counts_whitespace(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   ")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_max_length_boundary_100(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="x" * 100)

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 100)

    def test_external_id_length_raises_type_error_if_not_string_or_none(self):
        # Caso anómalo: asignación indebida en memoria.
        # Precondiciones
        entry = LibraryEntry(external_game_id=123)

        # Llamada
        # Comprobaciones
        with self.assertRaises(TypeError):
            entry.external_id_length()


class LibraryEntryExternalIdUpperTests(TestCase):
    def test_external_id_upper_converts_regular_string_to_uppercase(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc123")

        # Llamada
        upper_id = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(upper_id, "ABC123")

    def test_external_id_upper_handles_empty_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        upper_id = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(upper_id, "")

    def test_external_id_upper_handles_none_as_empty_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id=None)

        # Llamada
        upper_id = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(upper_id, "")


class LibraryEntryHoursPlayedLabelTests(TestCase):
    def test_hours_played_label_returns_none_for_zero_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=0)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "none")

    def test_hours_played_label_returns_low_for_less_than_ten_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=5)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "low")

    def test_hours_played_label_returns_high_for_ten_or_more_hours(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=15)

        # Llamada
        label = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(label, "high")


class LibraryEntryStatusValueTests(TestCase):
    def test_status_value_returns_zero_for_wishlist(self):
        # Precondiciones
        entry = LibraryEntry(status=LibraryEntry.STATUS_WISHLIST)

        # Llamada
        value = entry.status_value()

        # Comprobaciones
        self.assertEqual(value, 0)

    def test_status_value_returns_one_for_playing(self):
        # Precondiciones
        entry = LibraryEntry(status=LibraryEntry.STATUS_PLAYING)

        # Llamada
        value = entry.status_value()

        # Comprobaciones
        self.assertEqual(value, 1)

    def test_status_value_returns_minus_one_for_invalid_status(self):
        # Precondiciones
        entry = LibraryEntry(status="invalid")

        # Llamada
        value = entry.status_value()

        # Comprobaciones
        self.assertEqual(value, -1)

