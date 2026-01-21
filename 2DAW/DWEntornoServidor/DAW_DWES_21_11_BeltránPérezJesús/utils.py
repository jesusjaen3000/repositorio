import datetime
from typing import List
from models import Cliente, Pedido, DB_CLIENTES, DB_PEDIDOS

def crear_cliente(nif: str, nombre: str, email: str, activo: bool = True) -> Cliente:
    """Crea y guarda un nuevo objeto Cliente."""
    cliente = Cliente(nif=nif, nombre=nombre, email=email, activo=activo)
    DB_CLIENTES.append(cliente) 
    print(f"✅ Cliente creado: {cliente}")
    return cliente

def crear_pedido(cliente: Cliente, codigo: str, importe_total: float, estado: str = 'Pendiente') -> Pedido:
    """Crea y guarda un nuevo objeto Pedido asociado a un cliente existente."""
    if cliente not in DB_CLIENTES:
        raise ValueError("El objeto Cliente proporcionado no existe en la base de datos simulada.")
    
    pedido = Pedido(cliente=cliente, codigo=codigo, importe_total=importe_total, estado=estado)
    DB_PEDIDOS.append(pedido) 
    print(f"✅ Pedido creado: {pedido.codigo} para {cliente.nombre}")
    return pedido

def buscar_pedidos_minimo_importe(min_importe: float) -> List[Pedido]:
    """Busca y devuelve todos los pedidos con importe total mayor o igual al mínimo especificado."""
    return [p for p in DB_PEDIDOS if p.importe_total >= min_importe]

def buscar_clientes_con_pedidos_pagados() -> List[Cliente]:
    """Busca clientes que tengan al menos un pedido con estado 'Pagado'."""
    clientes_encontrados = set()
    
    for cliente in DB_CLIENTES:
        for pedido in cliente.pedidos:
            if pedido.estado.lower() == 'pagado':
                clientes_encontrados.add(cliente)
                break 
                
    return list(clientes_encontrados)

def limpiar_db():
    global DB_CLIENTES, DB_PEDIDOS, _NEXT_CLIENTE_ID, _NEXT_PEDIDO_ID
    DB_CLIENTES = []
    DB_PEDIDOS = []