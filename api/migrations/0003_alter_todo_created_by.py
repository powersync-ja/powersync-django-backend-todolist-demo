# Generated by Django 4.2.6 on 2023-10-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_todo_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_by',
            field=models.CharField(max_length=36, null=True),
        ),
    ]