from datetime import datetime
import os
from django.contrib import messages 
import shutil
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Videos, Historial
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
                
              
                usuario = request.user.id
                
                descripcion = "Inicia Sesión"
                tabla = "" 
                fechayhora = datetime.now()
                
                try:
                    his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
                    his.save()
                except Exception as e:
                    # Es buena práctica manejar errores al guardar en el historial
                    print(f"Error al guardar en el historial: {e}")
                
                return redirect('administrador')
            else:
                return render(request, 'paginas/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
        else:
            return render(request, 'paginas/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
    else:
        form = AuthenticationForm()
        return render(request, 'paginas/login.html', {'form': form})
    
@login_required
@permission_required('streaming.view_videos', raise_exception=True)
def administrador(request):
    videos = Videos.objects.all()
    return render(request, 'paginas/administrador.html', {'videos': videos})

def registrar_video(request):
    if request.method == 'POST':
        
        new_video_name = request.POST.get('name')
        uploaded_file = request.FILES.get('video')
        
       
        if not uploaded_file or not new_video_name:
            messages.error(request, 'Debes proporcionar un nombre y un archivo de video.')
            return redirect('administrador')
        
        
        extension = os.path.splitext(uploaded_file.name)[1]
        
      
        file_name = f"{new_video_name}{extension}"
        uploaded_file.name = file_name
        
        
        try:
            video = Videos(video_name=new_video_name, location=uploaded_file)
            video.save()
            
          
            if request.user.is_authenticated:
                usuario = request.user.id
                descripcion = (f"Registro del video: {new_video_name}")  
                tabla = "Videos" 
                fechayhora = datetime.now()
                
                historial_entry = Historial(
                    descripcion_historial=descripcion,
                    tabla_afectada_historial=tabla,
                    fecha_hora_historial=fechayhora,
                    usuario_id=usuario
                )
                historial_entry.save()
                
            messages.success(request, f'El video {new_video_name} fue guardado exitosamente.')
        except Exception as e:
            
            print(f"Error al guardar el video o el historial: {e}")
            messages.error(request, 'Ocurrió un error al guardar el video. Inténtalo de nuevo.')
            
        return redirect('administrador')
    
    # Si la solicitud no es POST, simplemente renderiza la página
    return render(request, 'paginas/administrador.html')
   
def editar_name_video(request, video_id): 
    
    video = get_object_or_404(Videos, video_id=video_id)

    if request.method == 'POST':
        try:
            new_video_name = request.POST.get('video_name')
            
            
            if new_video_name:
                video.video_name = new_video_name
                video.save()
                if request.user.is_authenticated:
                    usuario = request.user.id
                    descripcion = (f"edito el nombre del video {new_video_name}")  
                    tabla = "Videos" 
                    fechayhora = datetime.now()
                    
                    historial_entry = Historial(
                        descripcion_historial=descripcion,
                        tabla_afectada_historial=tabla,
                        fecha_hora_historial=fechayhora,
                        usuario_id=usuario
                    )
                    historial_entry.save()
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
        if request.user.is_authenticated:
                usuario = request.user.id
                descripcion = ( f'elimino el video: {video_titulo}')  
                tabla = "Videos" 
                fechayhora = datetime.now()
                
                historial_entry = Historial(
                    descripcion_historial=descripcion,
                    tabla_afectada_historial=tabla,
                    fecha_hora_historial=fechayhora,
                    usuario_id=usuario
                )
                historial_entry.save()
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
        
        
        if not all([first_name, username, password, rol_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('usuarios')
        
        
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('usuarios')
            
        
        if not username.isalnum():
            messages.error(request, 'El nombre de usuario solo puede contener letras y números.')
            return redirect('usuarios')
            
        
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
                 
                if request.user.is_authenticated:
                    usuario = request.user.id
                    descripcion = ( f'se registro el usuaio : {username}')  
                    tabla = "auth_user" 
                    fechayhora = datetime.now()
                    
                    historial_entry = Historial(
                        descripcion_historial=descripcion,
                        tabla_afectada_historial=tabla,
                        fecha_hora_historial=fechayhora,
                        usuario_id=usuario
                    )
                    historial_entry.save()

                messages.success(request, f'El usuario {username} ha sido registrado exitosamente.')
                return redirect('usuarios')
            
        except Exception as e:
            messages.error(request, f'Error inesperado al registrar el usuario: {str(e)}')
            return redirect('usuarios')
        
    return render(request, 'paginas/usuarios.html')


def registrar_grupo(request):
    if request.method == 'POST':
        nombre_rol = request.POST.get('nombre_rol')
        permisos_seleccionados = request.POST.getlist('permisos')

        if not nombre_rol:
            messages.error(request, 'El nombre del rol no puede estar vacío.')
            return redirect('usuarios')

        try:
           
            group, created = Group.objects.get_or_create(name=nombre_rol) 
            permisos_db = Permission.objects.filter(codename__in=permisos_seleccionados)
            group.permissions.set(permisos_db)
            
            if request.user.is_authenticated:
                    usuario = request.user.id
                    descripcion = ( f'se registro el rol : {nombre_rol}')  
                    tabla = "auth_permission" 
                    fechayhora = datetime.now()
                    
                    historial_entry = Historial(
                        descripcion_historial=descripcion,
                        tabla_afectada_historial=tabla,
                        fecha_hora_historial=fechayhora,
                        usuario_id=usuario
                    )
                    historial_entry.save()

            if created:
                
                 messages.success(request, f'El grupo {nombre_rol} ha sido creado con éxito y los permisos han sido asignados.')
            else:
                messages.success(request, f'Los permisos para el grupo {nombre_rol} han sido actualizados con éxito.')
                
            return redirect('usuarios') # Redirecciona a una página de éxito
        
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
            return redirect('usuarios')

   
    return render(request, 'paginas/usuarios.html')

def eliminar_user_admin(request, id):
        user = get_object_or_404(User, id=id)
        if request.method == 'GET':
            username_delete = user.first_name
            user.delete()
            if request.user.is_authenticated:
                    usuario = request.user.id
                    descripcion = ( f'se elimino el usuario : {username_delete}')  
                    tabla = "auth_user" 
                    fechayhora = datetime.now()
                    
                    historial_entry = Historial(
                        descripcion_historial=descripcion,
                        tabla_afectada_historial=tabla,
                        fecha_hora_historial=fechayhora,
                        usuario_id=usuario
                    )
                    historial_entry.save()
            messages.success(request, f'El usuario {username_delete} fue eliminado exitosamente.')
            return redirect('usuarios')
        return render(request, 'paginas/usuarios.html', {'user': user})



def edit_user(request, id):
   
    user_to_update = get_object_or_404(User, id=id)

   
    current_group = user_to_update.groups.first()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        rol_id = request.POST.get('rol') 

        if first_name and first_name != user_to_update.first_name:
            user_to_update.first_name = first_name
        
        if username and username != user_to_update.username:
            user_to_update.username = username
            
        if password and password != user_to_update.password:
            user_to_update.set_password(password)

       
        if rol_id:
            try:
                new_group = Group.objects.get(id=rol_id)
                user_to_update.groups.clear()
                user_to_update.groups.add(new_group)
            except Group.DoesNotExist:
                messages.error(request, 'El rol seleccionado no es válido.')
        
        user_to_update.save()
        if request.user.is_authenticated:
                    usuario = request.user.id
                    descripcion = ( f'se edito el usuario : {user_to_update}')  
                    tabla = "auth_user" 
                    fechayhora = datetime.now()
                    
                    historial_entry = Historial(
                        descripcion_historial=descripcion,
                        tabla_afectada_historial=tabla,
                        fecha_hora_historial=fechayhora,
                        usuario_id=usuario
                    )
                    historial_entry.save()
        
        messages.success(request, 'El usuario se actualizó exitosamente.')
        return redirect('usuarios') 
    
   
    groups = Group.objects.all()
    return render(request, 'paginas/usuario.html', {
        'current_group': current_group,
    })
        
        

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


@login_required
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


def history(request):
    historial = Historial.objects.all()
    x={
      'historial':historial  
    }
    return render(request, 'paginas/history.html', x)


    
    

def logout_view(request):
    if request.user.is_authenticated:
        try:
          
            usuario = request.user.id
            descripcion = "Cierra Sesión"  
            tabla = ""  
            fechayhora = datetime.now()
            
            
            his = Historial(
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
            his.save()
        except Exception as e:
            
            print(f"Error al guardar en el historial: {e}")
            pass 
            
  
    logout(request)
    return redirect('inicio')