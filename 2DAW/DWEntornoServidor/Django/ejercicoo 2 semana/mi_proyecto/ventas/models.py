# ventas/models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal

class Cliente(models.Model):
    nif = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.nif})"

    # Devuelve QuerySet con los pedidos filtrados por estado
    def pedidos_por_estado(self, estado):
        return self.pedidos.filter(estado=estado)

    # Suma los importes de los pedidos con estado PAGADO (devuelve Decimal)
    def total_pagado(self):
        from django.db.models import Sum
        agregado = self.pedidos.filter(estado=Pedido.ESTADO_PAGADO).aggregate(total=Sum('importe_total'))
        return agregado['total'] or Decimal('0.00')

    # Activar / desactivar cliente
    def activar(self):
        if not self.activo:
            self.activo = True
            self.save(update_fields=['activo'])

    def desactivar(self):
        if self.activo:
            self.activo = False
            self.save(update_fields=['activo'])


class Pedido(models.Model):
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_PAGADO = 'PAGADO'
    ESTADO_CANCELADO = 'CANCELADO'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_CANCE_
