from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=24)
    email = models.CharField(max_length=120)
    observacao = models.TextField()
    criado_em = models.DateField(auto_now_add=True)
    atualizado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Atendente(models.Model):
    nome_atend = models.CharField(max_length=120, null=False)
    telefone_atend = models.CharField(max_length=24, null=False)
    observacao_atend = models.TextField(null=False)
    criado_em_atend = models.DateTimeField(auto_now_add=True)
    atualizado_em_atend = models.DateTimeField(auto_now_add=True)
    ativo_atend = models.BooleanField()
    user_atend = models.ForeignKey(get_user_model(), null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome_atend

