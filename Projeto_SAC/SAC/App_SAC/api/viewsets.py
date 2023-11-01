from rest_framework import viewsets
from App_SAC.api import serializers
from App_SAC import models
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClienteSerializer
    queryset = models.Cliente.objects.all()

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['nome', 'telefone', 'email']

    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'telefone', 'email', 'observacao']


class AtendimentoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AtendimentoSerializer
    queryset = models.Atendimento.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente__nome', 'cliente__telefone', 'cliente__email', 'cliente__observacao', 'solicitacao']
