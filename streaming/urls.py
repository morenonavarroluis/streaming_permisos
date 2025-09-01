from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views
urlpatterns = [
    path('', views.videos, name='video'),
    path('inicio', views.inicio, name='inicio'),
    path('administrador', views.administrador, name='administrador'),
    path('registrar_video', views.registrar_video, name='registrar_video'),
    path('editar_name_video/<int:video_id>', views.editar_name_video, name='editar_name_video'),
    path('eliminar_video/<int:video_id>' , views.eliminar_video, name='eliminar_video'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('registrar_usuario', views.registrar_usuario , name='registrar_usuario'),
    path('registrar_grupo', views.registrar_grupo , name='registrar_grupo'),
    path('eliminar_user_admin/<int:id>', views.eliminar_user_admin , name='eliminar_user_admin'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('espacio_disco', views.espacio_disco, name='espacio_disco'),
    path('perfil', views.perfil, name='perfil'),
    path('history', views.history, name='history'),
    path('logout', views.logout_view, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
