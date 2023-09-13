from django.urls import path
from . import views
from .views import CustomLoginView, register_user, doctor_dashboard,ficha_paciente
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', register_user, name="signup"),
    path('familiar_dashboard/', views.familiar_dashboard, name='familiar_dashboard'),
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('familiar/pagina_de_error/', views.pagina_de_error, name='pagina_de_error'),
    path('ficha_paciente/<int:paciente_id>/', ficha_paciente, name='ficha_paciente'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('crear_paciente/', views.crear_paciente, name='crear_paciente'),
    path('lista_pacientes_sin_doctor/', views.lista_pacientes_sin_doctor, name='lista_pacientes_sin_doctor'),
    path('tomar_paciente_y_ficha/<int:paciente_id>/', views.tomar_paciente_y_ficha, name='tomar_paciente_y_ficha'),    
    path('subir_archivo/', views.subir_archivo, name='subir_archivo'),
    path('lista_archivos/', views.lista_archivos, name='lista_archivos'),
]