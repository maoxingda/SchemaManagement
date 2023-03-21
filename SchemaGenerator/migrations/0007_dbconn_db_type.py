# Generated by Django 4.1 on 2023-03-21 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchemaGenerator', '0006_alter_table_conn'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbconn',
            name='db_type',
            field=models.CharField(choices=[('MySQL', 'Mysql'), ('PostgreSQL', 'Postgresql')], default='PostgreSQL', max_length=16, verbose_name='数据库类型'),
        ),
    ]