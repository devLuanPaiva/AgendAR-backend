# Generated by Django 5.0.6 on 2024-05-24 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agendamentos', '0002_alter_agendamentospeloestabelecimento_nome'),
        ('Horarios', '0002_alter_horario_turno'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamentospelocliente',
            name='horario',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='Horarios.horario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agendamentospeloestabelecimento',
            name='horario',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='Horarios.horario'),
            preserve_default=False,
        ),
    ]
