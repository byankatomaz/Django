from . import views
from django.urls import path

urlpatterns = [
    path('', views.abrir_index, name='abrir_index'),
    path('cad_cliente', views.cad_cliente, name='cad_cliente'),
    path('salvar_cliente_novo', views.salva_cliente_novo, name='salvar_cliente_novo'),
    path('cons_cliente', views.cons_cliente, name='cons_cliente'),
    path('edit_cliente/<int:id>', views.edit_cliente, name='edit_cliente'),
    path('salvar_cliente_editado', views.salvar_cliente_editado, name='salvar_cliente_editado'),
    path('delete_cliente/<int:id>', views.delete_cliente, name='delete_cliente'),
    
    path('cad_atend', views.cad_atend, name='cad_atend'),
    path('salvar_atend_novo', views.salvar_atend_novo, name='salvar_atend_novo'),
    path('cons_atend', views.cons_atend, name='cons_atend'),
    path('edit_atend/<int:id>', views.edit_atend, name='edit_atend'),
    path('salvar_atend_editado', views.salvar_atend_editado, name='salvar_atend_editado'),
    
    path('cad_depto', views.cad_depto, name='cad_depto'),
    path('salvar_depto_novo', views.salvar_depto_novo, name='salvar_depto_novo'),
    path('cons_depto', views.cons_depto, name='cons_depto'),
    path('edit_depto/<int:id>', views.edit_depto, name='edit_depto'),
    path('salvar_depto_editado', views.salvar_depto_editado, name='salvar_depto_editado'),

    path('cad_situacao', views.cad_situacao, name='cad_situacao'),
    path('salvar_situacao_novo', views.salvar_situacao_novo, name='salvar_situacao_novo'),
    path('cons_situacao', views.cons_situacao, name='cons_situacao'),
    path('edit_situacao/<int:id>', views.edit_situacao, name='edit_situacao'),
    path('salvar_situacao_editado', views.salvar_situacao_editado, name='salvar_situacao_editado'),
    
    path('reg_atend_busca', views.reg_atend_busca, name='reg_atend_busca'),
    
]