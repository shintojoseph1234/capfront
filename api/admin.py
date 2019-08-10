from django.contrib import admin
from api.models import (Employees, Departments, Dept_emp, Titles, Salaries)

# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(Employees)
admin.site.register(Departments)
admin.site.register(Dept_emp)
admin.site.register(Titles)
admin.site.register(Salaries)
