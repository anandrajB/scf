# Generated by Django 3.2.5 on 2021-12-29 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_remove_programs_wf_item'),
        ('accounts', '0002_auto_20211229_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowitems',
            name='programs',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.programs'),
        ),
    ]
