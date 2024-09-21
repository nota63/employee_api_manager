# Generated by Django 5.1 on 2024-09-14 08:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0007_assets_user_employee_user_salaryslips_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('estimated_budget', models.IntegerField()),
                ('expected_results', models.FileField(blank=True, upload_to='expected_project_results/')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('initialized', 'initialized'), ('completed', 'completed'), ('in progress', 'in progress')], default='pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('employees', models.ManyToManyField(to='emp.employee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emp.project')),
            ],
        ),
    ]
