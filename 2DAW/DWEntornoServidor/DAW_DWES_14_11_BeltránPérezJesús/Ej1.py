class Producto:
    """Clase para representar un Producto con control de precio y stock."""
    
    def __init__(self, nombre: str, precio: float, stock: int):
        self._nombre = nombre
        if precio < 0:
            raise ValueError("El precio inicial no puede ser negativo.")
        self._precio = precio
        if stock < 0:
            raise ValueError("El stock inicial no puede ser negativo.")
        self._stock = stock
    
    @property
    def nombre(self):
        """Getter para nombre (solo lectura)."""
        return self._nombre

    @property
    def precio(self):
        """Getter para precio."""
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio: float):
        """Setter para precio. Lanza excepción si es negativo."""
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = nuevo_precio

    @property
    def stock(self):
        """Getter para stock."""
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        """Setter para stock. Lanza excepción si es negativo."""
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = nuevo_stock

def calcular_valor_inventario(inventario: list):
    """Recorre la lista y muestra el valor total (precio * stock) de cada producto."""
    print("\n--- Inventario y Valor Total ---")
    for producto in inventario:
        try:
            valor_total = producto.precio * producto.stock
            print(f"Producto: {producto.nombre}, Stock: {producto.stock}, Precio Unitario: ${producto.precio:.2f}, Valor Total: ${valor_total:.2f}")
        except Exception as e:
            print(f"Error al procesar el producto {producto.nombre}: {e}")

inventario = []

productos_a_crear = [
    ("Laptop", 1200.00, 15),
    ("Mouse", 25.50, 100),
    ("Teclado", 75.00, 50),
    ("Monitor", 300.00, -5), 
]

for nombre, precio, stock in productos_a_crear:
    try:
        producto = Producto(nombre, precio, stock)
        inventario.append(producto)
        print(f"✅ Creado: {nombre}")
    except ValueError as e:
        print(f"❌ Error al crear {nombre}: {e}")

calcular_valor_inventario(inventario)

print("\n--- Pruebas de Modificación ---")
if inventario:
    mi_producto = inventario[0]
    
    try:
        print(f"Stock actual de {mi_producto.nombre}: {mi_producto.stock}")
        mi_producto.stock = -10 
    except ValueError as e:
        print(f"❌ Error al actualizar el stock de {mi_producto.nombre}: {e}")
    finally:
        print(f"Stock después del intento: {mi_producto.stock}") 