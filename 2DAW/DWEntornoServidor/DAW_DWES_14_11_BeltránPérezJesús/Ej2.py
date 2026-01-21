class Alumno:
    """Clase para representar un Alumno y gestionar sus notas."""
    
    def __init__(self, nombre: str, notas: list = None):
        self._nombre = nombre
        self._notas = notas if notas is not None else []

    @property
    def nombre(self):
        """Getter para el nombre."""
        return self._nombre

    @property
    def notas(self):
        """Getter para las notas."""
        return self._notas

    def agregar_nota(self, nota: float):
        """Añade una nota a la lista, lanzando excepción si no está en [0, 10]."""
        if not (0 <= nota <= 10):
            raise ValueError("La nota debe estar entre 0 y 10.")
        self._notas.append(nota)
        print(f"Nota {nota} añadida a {self.nombre}.")

    def media(self):
        """Devuelve la nota media. Lanza excepción si la lista de notas está vacía."""
        if not self._notas:
            raise ZeroDivisionError(f"No hay notas para calcular la media de {self.nombre}.")
        
        return sum(self._notas) / len(self._notas)


alumno1 = Alumno("Ana García")
alumno2 = Alumno("Benito López")
alumno3 = Alumno("Carlos Ruiz")

print("\n--- Agregando Notas ---")
try:
    alumno1.agregar_nota(8.5)
    alumno1.agregar_nota(7.0)
    alumno1.agregar_nota(11.0) 
    alumno1.agregar_nota(9.0)
except ValueError as e:
    print(f"❌ Error al intentar agregar nota: {e}")

try:
    alumno2.agregar_nota(6.0)
    alumno2.agregar_nota(5.5)
    alumno2.agregar_nota(7.0)
except ValueError as e:
    print(f"❌ Error al intentar agregar nota: {e}")

alumnos = [alumno1, alumno2, alumno3] 

print("\n--- Notas Medias ---")
for alumno in alumnos:
    try:
        media = alumno.media()
        print(f"La media de {alumno.nombre} es: {media:.2f}")
    except ZeroDivisionError as e:
        print(f"⚠️ Advertencia para {alumno.nombre}: {e}")
    except Exception as e:
        print(f"❌ Error desconocido al calcular la media de {alumno.nombre}: {e}")