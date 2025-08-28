from datetime import datetime
import os
from django.contrib import messages 
import shutil
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Videos
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User ,Group , Permission
from django.db import transaction
from math import log, floor
from django.contrib.auth.decorators import permission_required


def videos(request):
    videos = Videos.objects.all()
    return render(request, 'paginas/videos.html', {'videos': videos})

def inicio(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('administrador') 

        else:
            return render(request, 'paginas/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})

    else:
        form = AuthenticationForm()
        return render(request, 'paginas/login.html', {'form': form})

@permission_required('streaming.view_videos', raise_exception=True)
def administrador(request):
    videos = Videos.objects.all()
    return render(request, 'paginas/administrador.html', {'videos': videos})

def registrar_video(request):
       if request.method == 'POST':
        video = Videos()
        
        
        new_video_name = request.POST.get('name')
        
        
        uploaded_file = request.FILES.get('video')
        
        if uploaded_file and new_video_name:
        
            extension = os.path.splitext(uploaded_file.name)[1]
            uploaded_file.name = new_video_name + extension
            
            
            video.video_name = new_video_name
            video.location = uploaded_file
            
           
            video.save()
            messages.success(request, f'El video "{new_video_name}" fue guardado exitosamente.')
            return redirect('administrador')
        else:
            messages.error(request, 'Debes proporcionar un nombre y un archivo de video.')
            return redirect('administrador')
            
       return render(request, 'paginas/administrador.html') 
   
def editar_name_video(request, video_id): 
    
    video = get_object_or_404(Videos, video_id=video_id)

    if request.method == 'POST':
        try:
            new_video_name = request.POST.get('video_name')
            
            
            if new_video_name:
                video.video_name = new_video_name
                video.save()
                messages.success(request, f'El nombre del video fue actualizado exitosamente a {new_video_name}.')
            else:
                
                messages.info(request, 'No se proporcionó un nuevo nombre. El nombre del video se mantuvo sin cambios.')
            
            return redirect('administrador')
        
        except Exception as e:
            messages.error(request, f'Ocurrió un error al actualizar el nombre: {e}')
            return redirect('usuarios')
    
    return render(request, 'paginas/admin.html', {'video': video})


def eliminar_video(request, video_id):
    
    video = get_object_or_404(Videos, video_id=video_id)
    
   
    if request.method == 'GET':
        video_titulo = video.video_name
        video.delete()
        messages.success(request, f'El video {video_titulo} fue eliminado exitosamente.')
        return redirect('administrador')
    return render(request, 'paginas/administrador.html', {'video': video})


@login_required
@permission_required('auth.view_user', raise_exception=True)
def usuarios(request):
    groups  = Group.objects.all()
    usuarios = User.objects.all()
    permiso = Permission.objects.all()
    contexto ={
        'usuarios': usuarios , 'groups':  groups , 'permiso': permiso
    }
    return render(request, 'paginas/usuarios.html', contexto)


def registrar_usuario(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        rol_id = request.POST.get('rol')
        print(rol_id)
        # Validación de campos vacíos
        if not all([first_name, username, password, rol_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('usuarios')
        
        # Validación de longitud mínima de password
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('usuarios')
            
        # Validación de formato de username
        if not username.isalnum():
            messages.error(request, 'El nombre de usuario solo puede contener letras y números.')
            return redirect('usuarios')
            
        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            return redirect('usuarios')

        try:
        
            with transaction.atomic():
             
                new_user = User.objects.create_user(
                    first_name = first_name,
                    username=username,
                    password=password,
                )

                
                rol_instance = get_object_or_404(Group, id=rol_id)
                new_user.groups.add(rol_instance)

               

                messages.success(request, f'El usuario {username} ha sido registrado exitosamente.')
                return redirect('usuarios')
            
        except Exception as e:
            messages.error(request, f'Error inesperado al registrar el usuario: {str(e)}')
            return redirect('usuarios')
        
    return render(request, 'paginas/usuarios.html')



def format_bytes(bytes_value, precision=2):
    """
    Convierte un valor en bytes a una unidad más legible (KB, MB, GB, TB).
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    bytes_value = max(bytes_value, 0)
    pow_val = floor((bytes_value if bytes_value > 0 else 0) / log(1024))
    pow_val = min(pow_val, len(units) - 1)
    bytes_value /= (1 << (10 * pow_val))
    return f"{bytes_value:.{precision}f} {units[pow_val]}"



def espacio_disco(request):
    """
    Vista que calcula el estado del disco y lo pasa al template.
    """
    # Lógica para la primera sección (espacio general)
    try:
        # Usa el directorio raíz de los archivos de medios como punto de referencia
        path_to_check = settings.BASE_DIR 
        
        disk_total_bytes, disk_used_bytes, disk_free_bytes = shutil.disk_usage(path_to_check)
        
        percentage_used = (disk_used_bytes / disk_total_bytes) * 100
        percentage_free = 100 - percentage_used
        
        main_disk_data = {
            'total': format_bytes(disk_total_bytes),
            'used': format_bytes(disk_used_bytes),
            'free': format_bytes(disk_free_bytes),
            'percentage_used': round(percentage_used, 2),
            'percentage_free': round(percentage_free, 2),
            'last_updated': datetime.now().strftime('%H:%M %d/%m/%Y'),
        }
    except Exception as e:
        # Manejo de errores si no se puede acceder a la información del disco
        main_disk_data = None
        print(f"Error al obtener el estado del disco: {e}")

    # Lógica para la segunda sección (particiones del sistema)
    partitions_list = []
    # Usamos una lista de directorios comunes para el ejemplo.
    # Puedes ajustarla según las necesidades de tu servidor.
    partitions_to_check = ['/', '/home', '/var', '/tmp'] 

    for path in partitions_to_check:
        if os.path.exists(path):
            try:
                total, used, free = shutil.disk_usage(path)
                percent = (used / total) * 100
                
                partitions_list.append({
                    'name': path,
                    'total': format_bytes(total),
                    'free': format_bytes(free),
                    'used': format_bytes(used),
                    'percent': round(percent, 2),
                    'bar_class': 'bg-danger' if percent > 90 else ('bg-warning' if percent > 70 else 'bg-success')
                })
            except Exception:
                continue

    context = {
        'main_disk_data': main_disk_data,
        'partitions': partitions_list,
    }

    return render(request, 'paginas/espacio.html', context)




def format_bytes(bytes_val, precision=2):
    if bytes_val == 0:
        return '0 B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB')
    i = int(floor(log(bytes_val, 1024)))
    p = pow(1024, i)
    s = round(bytes_val / p, precision)
    return f"{s} {size_name[i]}"

def perfil(request):
    return render(request, 'paginas/perfil.html')


    
    

def logout_view(request):
    logout(request)
    return redirect('inicio')