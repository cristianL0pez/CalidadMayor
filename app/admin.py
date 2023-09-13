from django.contrib import admin
from .models import Doctor, ProfesionalSalud, Cuidador, Paciente, FichaClinica, RegistroDiario,Archivo


# Register your models here.
admin.site.register(Doctor)
admin.site.register(ProfesionalSalud)
admin.site.register(Cuidador)
admin.site.register(Paciente)
admin.site.register(FichaClinica)
admin.site.register(RegistroDiario)
admin.site.register(Archivo)