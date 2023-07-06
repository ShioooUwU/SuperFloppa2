from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", home, name="home"),
    path("productos", productos, name="productos"),
    path("login", LoginView.as_view(template_name="core/login.html"), name="login"),    
    path("logout", logout, name="logout"),
    path("registro", registro, name="registro"),
    path("admin_producto", admin_prod, name="adminprod"),
    path("limpiar", limpiar, name="limpiar"),
    path("carrito", carrito, name="carrito"),
    path("comprar", comprar, name="comprar"),
    path("ventas", ventas, name="ventas"),
    path('eliminar_usuario/<usuario>/', eliminar_usuario, name='eliminar_usuario'),
    path("usuarioss", usuarioss, name="usuarioss"),
    path('modificar_producto/<codigo>/', modificar_producto, name='modificar'),
    path('eliminar_producto/<codigo>/', eliminar_producto, name='eliminar-producto'),
    path('agregar-producto/', agregar_producto, name="agregarp"),
    path("adminusuarios", adminusuarios, name="adminusuarios"),
    path('venta/<venta_id>/', detalle_venta, name='detalle_venta'),
    path('actualizar_usuario/<usuario>/', actualizar_usuario, name='actualizar_usuario'),
    path("adminproducto", adminproducto, name="adminproducto"),
    path("addtocar/<codigo>", addtocar, name="addtocar"),
    path("dropitem/<codigo>", dropitem, name="dropitem"),
    path("adminseguimientos", adminseguimientos, name="adminseguimientos"),
    path("suscribir", suscribir, name="suscribir"),
    path("modificar_seguimiento/<nro_seguimiento>/", modificar_seguimiento, name="modificar_seguimiento"),
]