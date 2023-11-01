from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('cad_cliente', views.cad_cliente, name='cad_cliente'),
    path('salvar_cliente_novo_prospect', views.salvar_cliente_novo_prospect, name='salvar_cliente_novo_prospect'),
    path('cons_cliente_prospect', views.cons_cliente_prospect, name='cons_cliente_prospect'),
    path('edit_cliente/<int:id>', views.edit_cliente, name='edit_cliente'),
    path('salvar_cliente_editado', views.salvar_cliente_editado, name='salvar_cliente_editado'),
    path('excluir_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),
    path('cad_atend', views.cad_atend, name='cad_atend'),
    path('salvar_atend_novo', views.salvar_atend_novo, name='salvar_atend_novo')
]
