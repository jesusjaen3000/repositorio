import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Cliente, Pedido
from utils import crear_cliente, crear_pedido, buscar_clientes_con_pedidos_pagados, buscar_pedidos_minimo_importe, limpiar_db

print("=====================================================")
print("=== DEMOSTRACIÓN DE ORM SIMULADO (shell_demo.py) ====")
print("=====================================================")

print("\n--- 0. Preparando y Limpiando Datos ---")
limpiar_db() 

cliente_a = crear_cliente(nif="111A", nombre="Alice Smith", email="alice@ejemplo.com")
cliente_b = crear_cliente(nif="222B", nombre="Bob Johnson", email="bob@ejemplo.com", activo=False)

crear_pedido(cliente=cliente_a, codigo="P001", importe_total=50.00, estado='Pagado')
crear_pedido(cliente=cliente_a, codigo="P002", importe_total=120.50, estado='Pendiente')
crear_pedido(cliente=cliente_a, codigo="P003", importe_total=10.00, estado='Pagado') 
crear_pedido(cliente=cliente_b, codigo="P004", importe_total=250.00, estado='Cancelado')
crear_pedido(cliente=cliente_b, codigo="P005", importe_total=30.00, estado='Pendiente')

print("\n--- 1. Relación Inversa (Cliente -> Pedidos) ---")
print(f"Pedidos de {cliente_a.nombre} (total: {len(cliente_a.pedidos)}):")
for p in cliente_a.pedidos:
    print(f"  - {p}")

print("\n--- 2. Filtrado con Métodos del Modelo Cliente ---")
pedidos_pagados = cliente_a.pedidos_por_estado('Pagado')
print(f"Pedidos PAGADOS de {cliente_a.nombre} ({len(pedidos_pagados)} encontrados):")
for p in pedidos_pagados:
    print(f"  - {p.codigo}")
    
total = cliente_a.total_pagado()
print(f"Total pagado por {cliente_a.nombre}: ${total:.2f}")

print("\n--- 3. Relación ForeignKey (Pedido -> Cliente) ---")
pedido_ejemplo = pedidos_pagados[0] # Usamos P001
print(f"Consultando el cliente del {pedido_ejemplo.codigo}:")
print(f"Cliente: {pedido_ejemplo.cliente.nombre} | Activo: {pedido_ejemplo.cliente.activo}")

print(f"¿{pedido_ejemplo.codigo} es válido (importe > 0)? {pedido_ejemplo.es_valido()}")

print("\n--- 4. Consultas Cruzadas (utils.py) ---")

clientes_con_pago = buscar_clientes_con_pedidos_pagados()
print(f"Clientes con al menos un pedido pagado ({len(clientes_con_pago)} encontrados):")
for c in clientes_con_pago:
    print(f"  - {c.nombre} (Activo: {c.activo})")

pedidos_caros = buscar_pedidos_minimo_importe(min_importe=150.00)
print(f"Pedidos con importe >= $150.00 ({len(pedidos_caros)} encontrados):")
for p in pedidos_caros:
    print(f"  - {p.codigo}: ${p.importe_total:.2f} (Cliente: {p.cliente.nombre})")
    
print("\n=====================================================")
print("=== DEMOSTRACIÓN COMPLETADA CON ÉXITO ====")
print("=====================================================")