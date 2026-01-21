# ventas/utils.py
from decimal import Decimal
from .models import Cliente, Pedido

def crear_cliente(nif, nombre, email=None, activo=True):
    cliente = Cliente(nif=nif, nombre=nombre, email=email, activo=activo)
    cliente.save()
    return cliente

def crear_pedido(cliente, codigo, importe_total=Decimal('0.00'), estado=Pedido.ESTADO_PENDIENTE, observaciones=''):
    if not isinstance(cliente, Cliente):
        raise ValueError("El argumento 'cliente' debe ser una instancia de Cliente.")
    pedido = Pedido(cliente=cliente, codigo=codigo, importe_total=Decimal(importe_total), estado=estado, observaciones=observaciones)
    pedido.save()
    return pedido

def buscar_pedidos_minimo_importe(min_importe):
    min_val = Decimal(min_importe)
    return Pedido.objects.filter(importe_total__gte=min_val)

def buscar_clientes_con_pedidos_pagados():
    return Cliente.objects.filter(pedidos__estado=Pedido.ESTADO_PAGADO).distinct()
