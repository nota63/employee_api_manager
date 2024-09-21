from django.contrib import admin
from .models import Employee, Document, Assets,SalarySlips, Project, Task
# Register your models here.
admin.site.register(Employee)
admin.site.register(Document)
admin.site.register(Assets)
admin.site.register(SalarySlips)
admin.site.register(Project)
admin.site.register(Task)
