# Generated by Django 5.0.6 on 2024-05-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Servicos', '0002_alter_servicos_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicos',
            name='nome',
            field=models.CharField(max_length=30),
        ),
    ]
