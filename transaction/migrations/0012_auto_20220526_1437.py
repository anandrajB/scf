# Generated by Django 3.2.5 on 2022-05-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_alter_workevents_record_datas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workevents',
            name='last_event',
        ),
        migrations.RemoveField(
            model_name='workflowitems',
            name='last_event',
        ),
        migrations.AddField(
            model_name='workevents',
            name='is_read',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='workflowitems',
            name='is_read',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
