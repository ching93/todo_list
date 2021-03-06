# Generated by Django 2.1.1 on 2018-10-03 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_todo_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.TextField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='text',
            field=models.TextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.TextField(max_length=100),
        ),
    ]
