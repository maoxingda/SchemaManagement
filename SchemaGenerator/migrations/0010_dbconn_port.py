# Generated by Django 4.1 on 2023-03-21 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchemaGenerator', '0009_dbconn_password_dbconn_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbconn',
            name='port',
            field=models.SmallIntegerField(default=5432, verbose_name='端口号'),
        ),
    ]
