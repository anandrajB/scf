# Generated by Django 3.2.5 on 2022-06-08 05:12

from django.db import migrations, models
import transaction.models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0012_auto_20220526_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceuploads',
            name='attached_file',
            field=models.FileField(default=1, upload_to=transaction.models.invoice_upload_file_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pairings',
            name='attached_file',
            field=models.FileField(default=1, upload_to=transaction.models.pairing_file_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programs',
            name='attached_file',
            field=models.FileField(default=1, upload_to=transaction.models.program_file_path),
            preserve_default=False,
        ),
    ]
