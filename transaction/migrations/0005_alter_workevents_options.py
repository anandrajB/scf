# Generated by Django 3.2.5 on 2022-05-20 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_auto_20220520_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workevents',
            options={'ordering': ['id'], 'verbose_name_plural': 'WorkEvent'},
        ),
    ]
