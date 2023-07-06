from django.shortcuts import render
from .models import *
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect, get_object_or_404
from .forms import *
from django.db.models import F
from django.shortcuts import redirect
#pip install requests
import requests






def eliminar_producto(request,codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.delete()
    return redirect(to="adminprod")

def agregar_producto(request):
    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES) 
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "guardado correctamente"
        else:
            data['form'] = formulario
            
    return render(request, 'core/agregarp.html', data)

def modificar_producto(request,codigo):
    
    producto = get_object_or_404(Producto, codigo=codigo)

    data = {
       'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='adminprod')
        data['form'] = formulario

    return render(request, 'core/modificar.html', data)


def eliminar_usuario(request, usuario):
    usuario = User.objects.get(username=usuario)
    usuario.delete()
    return redirect(to='usuarioss')

def usuarioss(request): 
    
    usuario = User.objects.all()
    
    return render(request, 'core/usuarioss.html', {'usuario':usuario}) 

def actualizar_usuario(request, usuario):
    if request.method == 'POST':
        usuario = User.objects.get(username=usuario)
        usuario.username = request.POST['usuario']
        usuario.first_name = request.POST['nombre']
        usuario.last_name = request.POST['apellido']
        usuario.email = request.POST['email']
        # Actualiza otros atributos del usuario según sea necesario
        usuario.save()
        return redirect('usuarioss')  # Redirige a la vista que muestra los usuarios nuevamente

    return redirect('usuarioss')  # Si no es una solicitud POST, redirige también


def ventas(request):
   
     
    if not request.user.is_authenticated:
        return redirect(to="login")
    venta = Venta.objects.all()
    
    return render(request, 'core/ventas.html',{'venta':venta})

def adminseguimientos(request):
    seguimientos = Seguimiento.objects.all()
    return render(request, 'core/adminseguimientos.html', {'seguimientos': seguimientos})

def modificar_seguimiento(request, nro_seguimiento):
    seguimiento = get_object_or_404(Seguimiento, nro_seguimiento=nro_seguimiento)

    if request.method == 'POST':
        seguimiento.estado = request.POST['estado']
        seguimiento.save()
        return redirect(to='adminseguimientos')

    return render(request, 'core/modificar_seguimiento.html', {'seguimiento': seguimiento})



def comprar(request):
    if not request.user.is_authenticated:
        return redirect(to="login")

    carro = request.session.get("carro", [])
    total = 0
    insufficient_stock = False

    for item in carro:
        total += item[5]
        producto = get_object_or_404(Producto, codigo=item[0])
        if producto.stock < item[4]: 
            insufficient_stock = True
            break

    if insufficient_stock:
        request.session["insufficient_stock"] = True
        return redirect(to="carrito")

    venta = Venta()
    venta.total = total
    venta.cliente = request.user
    venta.save()

    for item in carro:
        detalle = Detalle()
        detalle.venta = venta
        detalle.producto = get_object_or_404(Producto, codigo=item[0])
        detalle.precio = item[3]
        detalle.cantidad = item[4]
        detalle.save()

        producto = detalle.producto
        producto.stock -= detalle.cantidad
        producto.save()

    seguimiento = Seguimiento()
    seguimiento.id = venta
    seguimiento.estado = "Confirmando pago"
    seguimiento.save()

    request.session["carro"] = []
    return redirect(to="carrito")



def dropitem(request, codigo):
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == codigo:
            if item[4] > 1:
                item[4] -= 1
                item[5] = item[3] * item[4]
            else:
                carro.remove(item)
            request.session["carro"] = carro
            return redirect(to="carrito")
            
        
def addtocar(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    carro = request.session.get("carro", [])

    for item in carro:
        if item[0] == codigo:
            item[4] += 1
            item[5] = item[3] * item[4]
            break
    else:
        carro.append([codigo, producto.descripcion, producto.imagen, producto.precio, 1, producto.precio])
        
        if producto.stock < 1:
            return redirect(to="productos")  

    request.session["carro"] = carro
    return redirect(to="productos")

def home(request):
    context = {}
    suscrito(request, context)
    print(context)
    return render(request, "core/home.html", context)

def suscribir(request):
     context = {}
      
     if request.method == "POST":
        if request.user.is_authenticated:
            resp = requests.get(f"http://127.0.0.1:8000/api/suscribir/{request.user.email}") 
            context["mensaje"] = resp.json()["mensaje"]
            suscrito(request, context)
        return render(request, 'core/suscripcion.html',context)
     else:
            suscrito(request, context)
            return render(request, 'core/suscripcion.html', context)

def suscrito(request, context):
    if request.user.is_authenticated:
        email = request.user.email
        resp = requests.get(f"http://127.0.0.1:8000/api/suscrito/{email}")
        context["suscrito"] = resp.json()["suscrito"]



def carrito(request):
    context={}
    carro = request.session.get("carro", [])
    suscrito(request, context)
    context["carro"] = carro
    insufficient_stock = request.session.get("insufficient_stock", False)
    return render(request, 'core/carrito.html', {"insufficient_stock": insufficient_stock})

def limpiar(request):
    request.session.flush()
    return redirect(to="home")

# Create your views here.
def registro(request):
    if request.method == "POST":
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="login")
    else:
        form = Registro()
    return render(request, 'core/registro.html', {'form':form})

def productos(request):
    producto = Producto.objects.all()
    return render(request, 'core/productos.html', {'producto':producto})

def admin_prod(request):
    producto = Producto.objects.all()
    return render(request, 'core/adminprod.html', {'producto':producto})

def detalle_venta(request, venta_id):
    seguimiento = Seguimiento.objects.get(id=venta_id)
    venta = get_object_or_404(Venta, pk=venta_id)
    detalle = Detalle.objects.filter(venta=venta_id)  
    context = {'venta': venta, 'detalle': detalle, 'seguimiento': seguimiento}
    return render(request, 'core/detalle_venta.html', context)

def logout(request):
    return logout_then_login(request, login_url="home")

def adminusuarios(request): 

    return render(request, 'core/usuarios.html')

def adminproducto(request): 
    producto = Producto.objects.all()
    return render(request, 'core/adminproducto.html')