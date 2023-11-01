from rest_framework import serializers
from App_SAC import models


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cliente
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departamento
        fields = '__all__'


class AtendenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendente
        fields = '__all__'


class Situacao_AtendimentoSerializer(serializers.ModelSerializer):
    # id_atendente = AtendenteSerializer(read_only=True)
    # id_depto = DepartamentoSerializer(read_only=True)

    class Meta:
        model = models.Situacao_Atendimento
        fields = '__all__'


class AtendimentoSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField(read_only=True)
    departamento = serializers.StringRelatedField(read_only=True)
    atendente = serializers.StringRelatedField(read_only=True)
    atendimentos = Situacao_AtendimentoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Atendimento
        # fields = '__all__'
        fields = ['id', 'solicitacao', 'cliente', 'departamento', 'atendente', 'criado_em', 'encerrado', 'atendimentos']

