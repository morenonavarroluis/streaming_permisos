from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views
urlpatterns = [
    path('', views.videos, name='video'),
    path('inicio', views.inicio, name='inicio'),
    path('administrador', views.administrador, name='administrador'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('espacio_disco', views.espacio_disco, name='espacio_disco'),
    path('perfil', views.perfil, name='perfil'),
    path('logout', views.logout_view, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
