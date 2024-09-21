# Generated by Django 5.1.1 on 2024-09-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0013_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='body',
        ),
        migrations.AddField(
            model_name='email',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('failed', 'failed')], default='delivered', max_length=100, null=True),
        ),
    ]
