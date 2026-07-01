from django.shortcuts import render, redirect, get_object_or_404
from .models import Cargo, Empleado
from .forms import CargoForm, EmpleadoForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# ==========================================
# AUTENTICACIÓN (Registro, Login, Logout)
# ==========================================

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente tras registrarse
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

# ==========================================
# HOME / INDEX
# ==========================================
def home(request):
    return render(request, 'home.html')

# ==========================================
# CRUD DE CARGOS PROTEGIDO POR USUARIO
# ==========================================

@login_required
def cargo_list(request):
    # Solo trae los cargos creados por el usuario logueado
    cargos = Cargo.objects.filter(usuario=request.user)
    return render(request, 'cargos/cargo_list.html', {'cargos': cargos})

@login_required
def cargo_create(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.usuario = request.user  # Asigna automáticamente el usuario logueado
            cargo.save()
            return redirect('cargo_list')
    else:
        form = CargoForm()
    return render(request, 'cargos/cargo_form.html', {'form': form, 'titulo': 'Registrar Cargo'})

@login_required
def cargo_update(request, pk):
    # get_object_or_404 con el filtro de usuario evita que editen IDs de otros usuarios
    cargo = get_object_or_404(Cargo, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('cargo_list')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'cargos/cargo_form.html', {'form': form, 'titulo': 'Editar Cargo'})

@login_required
def cargo_delete(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cargo.delete()
        return redirect('cargo_list')
    return render(request, 'cargos/cargo_confirm_delete.html', {'objeto': cargo})


# ==========================================
# CRUD DE EMPLEADOS PROTEGIDO POR USUARIO
# ==========================================

@login_required
def empleado_list(request):
    # Solo trae los empleados creados por el usuario logueado
    empleados = Empleado.objects.filter(usuario=request.user)
    return render(request, 'empleados/empleado_list.html', {'empleados': empleados})

@login_required
def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, user=request.user) # Pasamos el usuario al formulario
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.usuario = request.user  # Asigna automáticamente el usuario logueado
            empleado.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm(user=request.user) # Pasamos el usuario al formulario
    return render(request, 'empleados/empleado_form.html', {'form': form, 'titulo': 'Registrar Empleado'})

@login_required
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm(instance=empleado, user=request.user)
    return render(request, 'empleados/empleado_form.html', {'form': form, 'titulo': 'Editar Empleado'})

@login_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk, usuario=request.user)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleado_list')
    return render(request, 'empleados/emple_confirm_delete.html', {'objeto': empleado})


# ==============================================================================
# SEGUNDA ETAPA: CRUD UTILIZANDO VISTAS BASADAS EN CLASES (VBC)
# ==============================================================================

# ----------------------------------------------
# VBC - CRUD DE CARGOS
# ----------------------------------------------

class CargoListView(LoginRequiredMixin, ListView):
    model = Cargo
    template_name = 'cargos/cargo_list_vbc.html'  # Usaremos una plantilla específica para VBC
    context_object_name = 'cargos'

    def get_queryset(self):
        # Filtra para que el usuario solo vea sus propios cargos
        return Cargo.objects.filter(usuario=self.request.user)


class CargoCreateView(LoginRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargo_form_vbc.html'
    success_url = reverse_lazy('cargo_list_vbc')

    def form_valid(self, form):
        # Asigna el usuario logueado automáticamente antes de guardar
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class CargoUpdateView(LoginRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargo_form_vbc.html'
    success_url = reverse_lazy('cargo_list_vbc')

    def get_queryset(self):
        # Evita que se editen cargos de otros usuarios mediante la URL
        return Cargo.objects.filter(usuario=self.request.user)


class CargoDeleteView(LoginRequiredMixin, DeleteView):
    model = Cargo
    template_name = 'cargos/cargo_confirm_delete_vbc.html'
    success_url = reverse_lazy('cargo_list_vbc')

    def get_queryset(self):
        # Evita que se eliminen cargos de otros usuarios mediante la URL
        return Cargo.objects.filter(usuario=self.request.user)


# ----------------------------------------------
# VBC - CRUD DE EMPLEADOS
# ----------------------------------------------

class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'empleados/empleado_list_vbc.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        return Empleado.objects.filter(usuario=self.request.user)


class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form_vbc.html'
    success_url = reverse_lazy('empleado_list_vbc')

    def get_form_kwargs(self):
        # Pasa el usuario actual al formulario para filtrar el select de Cargos
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form_vbc.html'
    success_url = reverse_lazy('empleado_list_vbc')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Empleado.objects.filter(usuario=self.request.user)


class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'empleados/emple_confirm_delete_vbc.html'
    success_url = reverse_lazy('empleado_list_vbc')

    def get_queryset(self):
        return Empleado.objects.filter(usuario=self.request.user)