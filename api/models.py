# Django imports
from django.db import models

class Employees(models.Model):
    MALE    = 'M'
    FEMALE  = 'F'
    gender_choices = [  (MALE, 'Male'),
                        (FEMALE, '"Female"')]

    emp_no      = models.IntegerField(models.Model, null=False, blank=False, primary_key=True)
    birth_date  = models.DateField(models.Model, max_length=200, null=False, blank=False)
    first_name  = models.CharField(models.Model, max_length=14, null=False, blank=False)
    last_name   = models.CharField(models.Model, max_length=16, null=False, blank=False)
    gender      = models.CharField(models.Model, choices=gender_choices, default=MALE, max_length=1)
    hire_date   = models.DateField(models.Model, max_length=15, null=False, blank=False)


class Departments(models.Model):
    dept_no     = models.CharField(models.Model, max_length=4, null=False, blank=False, primary_key=True)
    dept_name   = models.CharField(models.Model, max_length=40, unique=True)


class Dept_emp(models.Model):
    emp_no      = models.ForeignKey(Employees, on_delete=models.CASCADE)
    dept_no     = models.ForeignKey(Departments, on_delete=models.CASCADE)
    from_date   = models.DateField(models.Model, max_length=20, null=False, blank=False)
    to_date     = models.DateField(models.Model, max_length=20, null=False, blank=False)


class Titles(models.Model):
    emp_no      = models.ForeignKey(Employees, on_delete=models.CASCADE)
    title       = models.CharField(models.Model, max_length=50, null=False, blank=False, primary_key=True)
    from_date   = models.DateField(models.Model, max_length=20, null=False, blank=False)
    to_date     = models.DateField(models.Model, max_length=20, null=True, blank=True)


class Salaries(models.Model):
    emp_no      = models.ForeignKey(Employees, on_delete=models.CASCADE)
    salary      = models.IntegerField(models.Model, null=False, blank=False)
    from_date   = models.DateField(models.Model, max_length=20, null=False, blank=False)
    to_date     = models.DateField(models.Model, max_length=20, null=False, blank=False)
