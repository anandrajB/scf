# Generated by Django 3.2.5 on 2022-03-01 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0016_programs_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='workevents',
            name='type',
            field=models.CharField(default=1, max_length=55),
            preserve_default=False,
        ),
    ]