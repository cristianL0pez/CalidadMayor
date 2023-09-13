from django.db import models
from django.contrib.auth.models import User

# Modelo para los Doctores
class Doctor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos para los doctores si es necesario

    def __str__(self):
        return self.usuario.username

# Modelo para los Profesionales de la Salud (enfermeras, etc.)
class ProfesionalSalud(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos para los profesionales de la salud si es necesario

    def __str__(self):
        return self.usuario.username

# Modelo para los Cuidadores
class Cuidador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos para los cuidadores si es necesario

    def __str__(self):
        return self.usuario.username
# Modelo para los Pacientes
class Paciente(models.Model):
    usuario = models.CharField(max_length=255)
    fecha_de_nacimiento = models.DateField()
    familiar = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pacientes',null=True)  # Relación con el familiar
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='pacientes',null=True)  # Relación con el doctor 

    def __str__(self):
        return self.usuario
    
# Modelo para la Ficha Clínica del Paciente
class FichaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    fecha_de_ingreso = models.DateField(auto_now_add=True)
    peso = models.FloatField()
    talla = models.FloatField()
    historia_clinica = models.TextField()
    examen_fisico = models.TextField()

    def __str__(self):
        return f"Ficha de {self.paciente.usuario}"


# Modelo para los Registros Diarios
class RegistroDiario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    contenido = models.TextField()
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro Diario de {self.paciente.usuario} - {self.creado_en}"




class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)  # Puedes usar 'video', 'pdf', 'word', etc.
    fecha_carga = models.DateTimeField(auto_now_add=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='media/repositorio/')  # Define la carpeta de destino

    def __str__(self):
        return self.nombre