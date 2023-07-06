from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=datetime.now())
    cliente = models.ForeignKey(to=User, on_delete=models.CASCADE)
    total = models.IntegerField()
    
    def __str__(self):
        return str(self.id)+" "+self.cliente.username+" "+str(self.fecha)
    
# Create your models here.
class Producto(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    descripcion = models.CharField(max_length=200)
    precio  = models.IntegerField()
    stock  = models.IntegerField()
    imagen  = models.CharField(max_length=200)
    oferta = models.BooleanField(default=False)
    
    def tachado(self):
        if self.oferta:
            return "$" + str(round(self.precio *0.95))
        else:
            return ""

    def __str__(self):
        return self.codigo+" - "+self.descripcion
    
class Detalle(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(to=Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(to=Producto, on_delete=models.CASCADE)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    
    def __str__(self):
        return str(self.id)+" "+self.producto.descripcion[0:10]+" "+str(self.venta.id)
    
class Seguimiento(models.Model):
    nro_seguimiento = models.AutoField(primary_key=True)
    id = models.ForeignKey(to=Venta, on_delete=models.CASCADE)
    estado = models.CharField(max_length=25)
    
    def __str__(self):
        return  str(self.nro_seguimiento)
