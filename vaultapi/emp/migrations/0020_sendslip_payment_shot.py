# Generated by Django 5.1.1 on 2024-09-22 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0019_sendslip_payment_method_sendslip_present_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendslip',
            name='payment_shot',
            field=models.FileField(null=True, upload_to='paymentshots/'),
        ),
    ]
