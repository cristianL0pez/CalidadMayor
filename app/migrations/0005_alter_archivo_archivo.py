# Generated by Django 4.0.2 on 2023-09-13 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_archivo_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(upload_to='media/repositorio/'),
        ),
    ]
