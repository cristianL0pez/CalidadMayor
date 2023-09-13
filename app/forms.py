from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FichaClinica, RegistroDiario, Paciente, Archivo


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['usuario', 'fecha_de_nacimiento']




class RegistroDiarioForm(forms.ModelForm):
    class Meta:
        model = RegistroDiario
        fields = ['contenido']


class FichaClinicaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all())
    
    class Meta:
        model = FichaClinica
        fields = ['peso', 'talla', 'historia_clinica', 'examen_fisico']



class TomarPacienteForm(forms.ModelForm):
    # Agrega los campos necesarios para la toma del paciente
    # Por ejemplo, puedes agregar un campo de selección para el paciente

    class Meta:
        model = FichaClinica  # Usa tu modelo FichaClinica en lugar de Paciente
        fields = ['peso', 'talla', 'historia_clinica', 'examen_fisico']

    # Si deseas agregar más campos al formulario, puedes hacerlo aquí


class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('nombre', 'tipo', 'archivo')