# ventas/admin.py
from django.contrib import admin
from .models import Cliente, Pedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nif', 'nombre', 'email', 'activo', 'fecha_alta')
    search_fields = ('nif', 'nombre', 'email')
    list_filter = ('activo',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cliente', 'importe_total', 'estado', 'fecha')
    search_fields = ('codigo', 'cliente__nombre')
    list_filter = ('estado',)
