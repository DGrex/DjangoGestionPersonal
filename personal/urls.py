from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    
    # URLs Cargos (Funciones)
    path('cargos/', views.cargo_list, name='cargo_list'),
    path('cargos/nuevo/', views.cargo_create, name='cargo_create'),
    path('cargos/editar/<int:pk>/', views.cargo_update, name='cargo_update'),  # <-- Corregido :
    path('cargos/eliminar/<int:pk>/', views.cargo_delete, name='cargo_delete'),  # <-- Corregido :
    
    # URLs Empleados (Funciones)
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleados/editar/<int:pk>/', views.empleado_update, name='empleado_update'),  # <-- Corregido :
    path('empleados/eliminar/<int:pk>/', views.empleado_delete, name='empleado_delete'),  # <-- Corregido :

    
    # URLs Cargos (Clases - VBC)
    
    path('vbc/cargos/', views.CargoListView.as_view(), name='cargo_list_vbc'),
    path('vbc/cargos/nuevo/', views.CargoCreateView.as_view(), name='cargo_create_vbc'),
    path('vbc/cargos/editar/<int:pk>/', views.CargoUpdateView.as_view(), name='cargo_update_vbc'),
    path('vbc/cargos/eliminar/<int:pk>/', views.CargoDeleteView.as_view(), name='cargo_delete_vbc'),
    
    # URLs Empleados (Clases - VBC)
    path('vbc/empleados/', views.EmpleadoListView.as_view(), name='empleado_list_vbc'),
    path('vbc/empleados/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_create_vbc'),
    path('vbc/empleados/editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='empleado_update_vbc'),
    path('vbc/empleados/eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='empleado_delete_vbc'),

]