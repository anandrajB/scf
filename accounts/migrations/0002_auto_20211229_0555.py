# Generated by Django 3.2.5 on 2021-12-29 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflowitems',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='workflowitems',
            name='last_name',
        ),
        migrations.AddField(
            model_name='workflowitems',
            name='state',
            field=models.CharField(default='Draft', max_length=100),
        ),
    ]
