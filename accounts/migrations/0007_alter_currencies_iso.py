# Generated by Django 3.2.5 on 2022-06-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20220608_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='iso',
            field=models.IntegerField(),
        ),
    ]
