# Generated by Django 4.2.4 on 2023-11-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_SAC', '0006_rename_ativo_departamento_departamento_ativo_depto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendente',
            name='observacao_atend',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='atendente',
            name='telefone_atend',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='atendimento',
            name='criado_em',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='atualizado_em',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
