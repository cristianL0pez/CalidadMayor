from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from .forms import  SignUpForm, RegistroDiarioForm, FichaClinicaForm, PacienteForm,TomarPacienteForm, ArchivoForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import FichaClinica ,RegistroDiario, Doctor,Paciente
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import FichaClinica, Archivo


class CustomLoginView(LoginView):
    template_name = 'home/login.html'  # Define el nombre de l
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Familiar').exists():
            return reverse('familiar_dashboard')  # Redirige al dashboard de familiares
        elif user.groups.filter(name='Doctor').exists():
            return reverse('doctor_dashboard')  # Redirige al dashboard de doctores
        else:
            return reverse('pagina_de_error')  # Redirige a una página de error por defecto si no se encuentra un grupo válido


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardar el usuario
            user.groups.add(Group.objects.get(name='Familiar'))  # Agregar al grupo "Familiar"
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=raw_password)
            login(request, user)  # Iniciar sesión automáticamente

            msg = 'User created successfully.'
            success = True

            # Redireccionar al dashboard correspondiente, por ejemplo:
            return redirect("familiar_dashboard")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "home/signup.html", {"form": form, "msg": msg, "success": success})


@login_required
def familiar_dashboard(request):
    # Obtén el usuario actual (familiar)
    familiar_actual = request.user
    
    # Filtra los pacientes asociados a este familiar
    pacientes_del_familiar = Paciente.objects.filter(familiar=familiar_actual)
    # Crear un diccionario para almacenar pacientes y sus registros diarios
    pacientes_con_registros = {}
    
    # Iterar sobre los pacientes y obtener sus registros diarios
    for paciente in pacientes_del_familiar:
        registros_diarios = RegistroDiario.objects.filter(paciente=paciente)
        pacientes_con_registros[paciente] = registros_diarios

    user_belongs_to_familiar_group = request.user.groups.filter(name='Familiar').exists()

    group = {
        'user_belongs_to_familiar_group': user_belongs_to_familiar_group,
    }
    
    return render(request, 'familiar/familiar_dashboard.html', {'pacientes_con_registros': pacientes_con_registros, 'group':group})

 
@login_required
def pagina_de_error(request):
    # Lógica para mostrar el dashboard de doctores
    return render(request, 'familiar/pagina_de_error.html')



@login_required
def doctor_dashboard(request):
    # Obtén el doctor actual (puedes cambiar esto según tus necesidades)
    doctor_actual = Doctor.objects.get(usuario=request.user)
    
    # Filtra los pacientes asociados a este doctor
    pacientes_del_doctor = Paciente.objects.filter(doctor=doctor_actual)

    user_belongs_to_doctor_group = request.user.groups.filter(name='Doctor').exists()

    group = {
        'user_belongs_to_doctor_group': user_belongs_to_doctor_group,
    }
    
    return render(request, 'doctor/doctor_dashboard.html', {'pacientes': pacientes_del_doctor, 'group':group})


def index(request):
    # Puedes pasar información adicional a la plantilla si es necesario
    contexto = {
        'titulo': 'Bienvenido a Nuestra Aplicación Clínica',
        'descripcion': 'Esta aplicación te permite gestionar fichas clínicas de pacientes de manera eficiente.',
    }
    return render(request, 'home/index.html', contexto)





@login_required
def ficha_paciente(request, paciente_id):
    # Obtener el paciente correspondiente al paciente_id o mostrar un error 404 si no existe
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    ficha_paciente = paciente.fichaclinica


        # Obtener registros diarios del paciente
    registros_diarios = RegistroDiario.objects.filter(paciente=paciente)

    if request.method == 'POST':
        formulario = RegistroDiarioForm(request.POST)
        if formulario.is_valid():
            registro_diario = formulario.save(commit=False)
            registro_diario.paciente = paciente
            registro_diario.creado_por = request.user
            registro_diario.save()
            return redirect('ficha_paciente', paciente_id=paciente_id)
    else:
        formulario = RegistroDiarioForm()
    
    # Renderizar la plantilla de la ficha del paciente y pasar el paciente como contexto
    return render(request, 'doctor/ficha_paciente.html', {'paciente': paciente, 'ficha_paciente': ficha_paciente, 'registros_diarios': registros_diarios, 'formulario': formulario})


@login_required
def agregar_registro_diario(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)

    if request.method == 'POST':
        formulario = RegistroDiarioForm(request.POST)
        if formulario.is_valid():
            registro_diario = formulario.save(commit=False)
            registro_diario.paciente = paciente
            registro_diario.creado_por = request.user
            registro_diario.save()
            return redirect('ficha_paciente', paciente_id=paciente_id)
    else:
        formulario = RegistroDiarioForm()

    return render(request, 'agregar_registro_diario.html', {'formulario': formulario, 'paciente': paciente})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.familiar = request.user
            paciente.save()
            return redirect('familiar_dashboard')  # Redirige a la lista de pacientes o a donde prefieras
    else:
        form = PacienteForm()
    return render(request, 'familiar/crear_paciente.html', {'form': form})
@login_required
def lista_pacientes_sin_doctor(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Doctor').exists():
        # Obtén la lista de pacientes sin doctor asignado (donde doctor es nulo)
        pacientes_sin_doctor = Paciente.objects.filter(doctor=None)

        return render(request, 'doctor/lista_pacientes_sin_doctor.html', {'pacientes_sin_doctor': pacientes_sin_doctor})

    return redirect('login')  # Redirige a la página de inicio de sesión si no es un usuario doctor o no está autenticado

@login_required
def tomar_paciente_y_ficha(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method == 'POST':
        ficha_clinica_form = TomarPacienteForm(request.POST)

        if ficha_clinica_form.is_valid():
            ficha_clinica = ficha_clinica_form.save(commit=False)
            ficha_clinica.paciente = paciente
            # Obtén el doctor actual (suponiendo que tienes una relación entre User y Doctor)
            doctor_actual = Doctor.objects.get(usuario=request.user)
            # Asocia el doctor actual con el paciente
            paciente.doctor = doctor_actual
            ficha_clinica.save()
            paciente.save()

            return redirect('lista_pacientes_sin_doctor')

    else:
        ficha_clinica_form = TomarPacienteForm()

    return render(request, 'doctor/tomar_paciente_y_ficha.html', {
        'ficha_clinica_form': ficha_clinica_form,
        'paciente': paciente,
    })
@login_required
def crear_ficha_clinica(request):
    if request.method == 'POST':
        form = FichaClinicaForm(request.POST)
        if form.is_valid():
            ficha_clinica = form.save()
            return redirect('detalle_ficha_clinica', pk=ficha_clinica.pk)
    else:
        form = FichaClinicaForm()
    return render(request, 'crear_ficha_clinica.html', {'form': form})


@login_required
def subir_archivo(request):
    if request.method == 'POST':
        archivo_form = ArchivoForm(request.POST, request.FILES)
        if archivo_form.is_valid():
            archivo = archivo_form.save(commit=False)
            archivo.propietario = request.user
            archivo.save()
            return redirect('lista_archivos')
    else:
        archivo_form = ArchivoForm()
    return render(request, 'capacitacion/subir_archivo.html', {'archivo_form': archivo_form})

@login_required
def lista_archivos(request):
    archivos = Archivo.objects.filter(propietario=request.user)
    return render(request, 'capacitacion/lista_archivos.html', {'archivos': archivos})