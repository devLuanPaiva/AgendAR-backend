# Generated by Django 5.0.6 on 2024-05-23 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0003_alter_estabelecimento_contato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estabelecimento',
            name='numeroEndereco',
        ),
    ]
