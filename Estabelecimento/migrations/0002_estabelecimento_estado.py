# Generated by Django 5.0.6 on 2024-05-12 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estabelecimento',
            name='estado',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
    ]
