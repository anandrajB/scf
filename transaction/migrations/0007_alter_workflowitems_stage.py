# Generated by Django 3.2.5 on 2022-02-11 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0006_auto_20220211_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflowitems',
            name='stage',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('AWAITING_APPROVAL', 'AWAITING_APPROVAL'), ('AWAITING_ACCEPTANCE', 'AWAITING_ACCEPTANCE'), ('ACCEPTED', 'ACCEPTED'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'), ('FINANCE_REQUESTED', 'FINANCE_REQUESTED'), ('FINANCED', 'FINANCED'), ('FINANCE_REJECTED', 'FINANCE_REJECTED'), ('SETTLED', 'SETTLED'), ('OVERDUE', 'OVERDUE'), ('AWAITING_SIGN_A', 'AWAITING_SIGN_A'), ('AWAITING_SIGN_B', 'AWAITING_SIGN_B'), ('AWAITING_SIGN_C', 'AWAITING_SIGN_C'), ('DELETED', 'DELETED'), ('SIGN_A', 'SIGN_A'), ('SIGN_B', 'SIGN_B'), ('SIGN_C', 'SIGN_C'), ('SUBMIT', 'SUBMIT'), ('MAKER', 'MAKER')], max_length=255),
        ),
    ]
