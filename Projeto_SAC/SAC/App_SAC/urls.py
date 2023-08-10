from . import views
from django.urls import path

urlpatterns = [
    path('', views.abrir_index, name='abrir_index'),
    path('cad_cliente', views.cad_cliente, name='cad_cliente'),
    path('salvar_cliente_novo', views.salva_cliente_novo, name='salvar_cliente_novo'),
]