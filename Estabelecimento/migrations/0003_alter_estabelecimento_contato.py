# Generated by Django 5.0.6 on 2024-05-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0002_estabelecimento_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estabelecimento',
            name='contato',
            field=models.CharField(max_length=12),
        ),
    ]
