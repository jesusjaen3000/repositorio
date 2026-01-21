class Libro:
    """Clase para representar un Libro con estado de préstamo (True/False)."""
    
    def __init__(self, titulo: str, autor: str):
        self._titulo = titulo
        self._autor = autor
        self._prestado = False 

    @property
    def titulo(self):
        return self._titulo
    
    @property
    def prestado(self):
        return self._prestado

    def prestar(self):
        """Marca el libro como prestado. Lanza excepción si ya lo está."""
        if self._prestado:
            raise Exception(f"El libro '{self._titulo}' ya está prestado.")
        self._prestado = True
        print(f"✅ Libro '{self._titulo}' prestado exitosamente.")

    def devolver(self):
        """Marca el libro como no prestado. Lanza excepción si ya está disponible."""
        if not self._prestado:
            raise Exception(f"El libro '{self._titulo}' ya estaba disponible (no prestado).")
        self._prestado = False
        print(f"✅ Libro '{self._titulo}' devuelto exitosamente.")
        
    def __str__(self):
        """Devuelve una representación legible del libro."""
        estado = "Prestado" if self._prestado else "Disponible"
        return f"'{self._titulo}' por {self._autor} - Estado: {estado}"

class Biblioteca:
    """Clase para gestionar una lista de objetos Libro."""
    
    def __init__(self):
        self._libros = []

    def agregar_libro(self, libro: Libro):
        """Añade un libro a la lista."""
        self._libros.append(libro)
        print(f"Libro '{libro.titulo}' añadido a la biblioteca.")

    def buscar_por_titulo(self, titulo: str) -> Libro | None:
        """Busca un libro por título y lo retorna."""
        for libro in self._libros:
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    def mostrar_libros(self):
        """Muestra el estado de todos los libros."""
        print("\n--- Listado de Libros en Biblioteca ---")
        if not self._libros:
            print("La biblioteca está vacía.")
            return
        for libro in self._libros:
            print(libro)

if __name__ == "__main__":
    biblioteca = Biblioteca()

    l1 = Libro("Cien años de soledad", "García Márquez")
    l2 = Libro("1984", "George Orwell")
    l3 = Libro("El Principito", "Antoine de Saint-Exupéry")

    biblioteca.agregar_libro(l1)
    biblioteca.agregar_libro(l2)
    biblioteca.agregar_libro(l3)

    biblioteca.mostrar_libros()

    print("\n--- Simulación de Préstamo ---")
    
    libro_a_prestar = biblioteca.buscar_por_titulo("1984")
    if libro_a_prestar:
        try:
            libro_a_prestar.prestar() 
            
            libro_a_prestar.prestar() 
            
        except Exception as e:
            print(f"❌ Error detectado: {e}")
            
        finally:
            print(f"Estado de '{libro_a_prestar.titulo}' después del proceso: {'Prestado' if libro_a_prestar.prestado else 'Disponible'}")


    print("\n--- Simulación de Devolución ---")

    libro_a_devolver = biblioteca.buscar_por_titulo("Cien años de soledad")
    if libro_a_devolver:
        try:
            libro_a_devolver.prestar()
        except Exception:
            pass 

        try:
            libro_a_devolver.devolver()
            
            libro_a_devolver.devolver() 
            
        except Exception as e:
            print(f"❌ Error detectado: {e}")
            
        finally:
            print(f"Estado de '{libro_a_devolver.titulo}' después del proceso: {'Prestado' if libro_a_devolver.prestado else 'Disponible'}")
     
    biblioteca.mostrar_libros()