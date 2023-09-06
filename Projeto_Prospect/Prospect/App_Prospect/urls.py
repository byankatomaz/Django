from . import views
from django.urls import path

urlpatterns = [
    path('', views.abrir_index, name='abrir_index'),
    path('cad_cliente', views.cad_cliente, name='cad_cliente'),
    path('salvar_cliente_novo_prospect', views.salvar_cliente_novo_prospect, name='salvar_cliente_novo_prospect'),
    path('cons_cliente', views.cons_cliente, name='cons_cliente'),
    path('edit_cliente/<int:id>', views.edit_cliente, name='edit_cliente'),
    path('salvar_cliente_editado', views.salvar_cliente_editado, name='salvar_cliente_editado'),
    path('delete_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),
]