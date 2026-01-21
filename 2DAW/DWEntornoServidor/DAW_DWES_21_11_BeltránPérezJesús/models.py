import datetime
from typing import List, Optional

DB_CLIENTES = []
DB_PEDIDOS = []

_NEXT_CLIENTE_ID = 1
_NEXT_PEDIDO_ID = 1

def _get_next_id(model_name: str) -> int:
    """Función auxiliar para simular auto-incremento de ID."""
    global _NEXT_CLIENTE_ID, _NEXT_PEDIDO_ID
    if model_name == 'Cliente':
        _id = _NEXT_CLIENTE_ID
        _NEXT_CLIENTE_ID += 1
        return _id
    elif model_name == 'Pedido':
        _id = _NEXT_PEDIDO_ID
        _NEXT_PEDIDO_ID += 1
        return _id
    return -1

# -------------------------------------------------------------------

class Cliente:
    def __init__(self, nif: str, nombre: str, email: str, activo: bool = True, fecha_alta: datetime.date = None):
        self.id = _get_next_id('Cliente')
        self.nif = nif
        self.nombre = nombre
        self.email = email
        self.activo = activo
        self.fecha_alta = fecha_alta or datetime.date.today()
        
        self.pedidos = [] 

    def __str__(self):
        estado = "ACTIVO" if self.activo else "INACTIVO"
        return f"Cliente({self.id}): {self.nombre} ({self.nif}) - {estado}"

    def pedidos_por_estado(self, estado: str) -> List['Pedido']:
        """Devuelve una lista de pedidos de este cliente filtrados por estado."""
        return [p for p in self.pedidos if p.estado.lower() == estado.lower()]

    def total_pagado(self) -> float:
        """Calcula la suma total de los importes de los pedidos con estado 'Pagado'."""
        pedidos_pagados = self.pedidos_por_estado('Pagado')
        return sum(p.importe_total for p in pedidos_pagados)

    def activar(self):
        """Marca el cliente como activo."""
        self.activo = True
        print(f"[{self.nombre}] marcado como ACTIVO.")

    def desactivar(self):
        """Marca el cliente como no activo."""
        self.activo = False
        print(f"[{self.nombre}] marcado como INACTIVO.")


class Pedido:
    ESTADOS = ['Pendiente', 'Pagado', 'Cancelado', 'Enviado']
    
    def __init__(self, cliente: Cliente, codigo: str, importe_total: float, estado: str = 'Pendiente', fecha: datetime.date = None):
        self.id = _get_next_id('Pedido')
        self.cliente = cliente 
        self.codigo = codigo
        self.fecha = fecha or datetime.date.today()
        self.importe_total = importe_total
        
        if estado not in self.ESTADOS:
            raise ValueError(f"Estado '{estado}' no válido. Debe ser uno de: {self.ESTADOS}")
        self.estado = estado

        self.cliente.pedidos.append(self)
        
    def __str__(self):
        return f"Pedido({self.id}): {self.codigo} - Cliente: {self.cliente.nombre} - Importe: {self.importe_total:.2f} - Estado: {self.estado}"

    def es_valido(self) -> bool:
        """Devuelve True si el importe total es mayor que 0."""
        return self.importe_total > 0

    def marcar_como_pagado(self):
        """Cambia el estado del pedido a 'Pagado'."""
        self.estado = 'Pagado'
        print(f"[Pedido {self.codigo}] Estado cambiado a PAGADO.")

    def cambiar_importe(self, nuevo_importe: float):
        """Cambia el valor del importe total del pedido."""
        if nuevo_importe < 0:
            raise ValueError("El importe no puede ser negativo.")
        self.importe_total = nuevo_importe
        print(f"[Pedido {self.codigo}] Importe actualizado a {self.importe_total:.2f}.")