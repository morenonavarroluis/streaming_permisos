from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.apps import apps
from django.db.utils import OperationalError
from django.contrib.contenttypes.models import ContentType

@receiver(post_migrate)
def translate_permissions(sender, **kwargs):
    # Mapeo de nombres de modelos a sus traducciones
    model_name_map = {
        'logentry': 'Entradas del registro',
        'group': 'Grupos',
        'permission': 'Permisos',
        'user': 'Usuarios',
        'contenttype': 'Tipos de contenido',
        'session': 'Sesiones',
        'videos': 'Videos',  # Nombre de tu modelo
    }

    # Mapeo de verbos de permisos
    verbs_map = {
        'add': 'agregar',
        'change': 'cambiar',
        'delete': 'borrar',
        'view': 'ver',
    }

    try:
        permissions = Permission.objects.all()
    except OperationalError:
        return

    for p in permissions:
     
        perm_parts = p.codename.split('_')
        verb = perm_parts[0]

       
        ct = p.content_type
        model_name = ct.model

    
        if model_name in model_name_map:
            translated_model_name = model_name_map[model_name]
            translated_verb = verbs_map.get(verb, verb) 

          
            p.name = f"{translated_verb} {translated_model_name}"
            p.save()