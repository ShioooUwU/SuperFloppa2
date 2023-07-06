from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class Registro(UserCreationForm):
    first_name = forms.CharField(max_length=40, help_text="Ingrese su nombre")
    last_name = forms.CharField(max_length=40, help_text="Ingrese su apellido")
    email = forms.EmailField(max_length=120, help_text="Ingrese su correo")


class Meta(UserCreationForm.Meta):
    model = User
    fields = ("username", "first_name", "last_name", "email", "password1", "password2")