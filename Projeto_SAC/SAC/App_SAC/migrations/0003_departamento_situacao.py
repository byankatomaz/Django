# Generated by Django 4.2.4 on 2023-09-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_SAC', '0002_atendente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_departamento', models.CharField(max_length=30)),
                ('info_departamento', models.TextField(null=True)),
                ('ativo_departamento', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Situacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_situacao', models.CharField(max_length=30)),
                ('info_situacao', models.TextField(null=True)),
                ('ativo_situacao', models.BooleanField()),
            ],
        ),
    ]
