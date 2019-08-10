# django imports
from rest_framework import serializers
# model imports
from api.models import Departments
# other imports
from datetime import date


class HikeEligibleSerializer(serializers.Serializer):
    employee_id         = serializers.IntegerField()


class EmployeeHireSerializer(serializers.Serializer):
    birth_date      = serializers.DateField()
    employee_id     = serializers.IntegerField(required=True)
    first_name      = serializers.CharField(max_length=14)
    last_name       = serializers.CharField(max_length=16)
    gender          = serializers.CharField(max_length=1)
    salary          = serializers.ListField(child=serializers.DateField())
    department      = serializers.CharField(max_length=40)
    title           = serializers.CharField(max_length=50)
    hire_date       = serializers.DateField()

    def validate(self, data):
        """
        Check that date_from is less than date_to
        """
        # date of birth of employee
        dob         = data['birth_date']
        # todays date
        today = date.today()
        # age of employee
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        # check whether age is between 18 to 60
        if  age < 18 or age > 60:
            # else raise and error message
            raise serializers.ValidationError(" employee age must be in the range of 18 to 60")

        # select the department
        department  = data['department']
        # find all in dept_name columns
        department_queryset = Departments.objects.values_list('dept_name', flat=True)
        # converting to lowercase
        department_list = [each.lower() for each in department_queryset]
        # if not in department_list
        if department.lower() not in department_list:
            # else raise and error message
            raise serializers.ValidationError(" department must be in any of these {}".format(department_list))

        # title for that employee
        title = data["title"]
        # title list
        titles_list = ["staff", "senior staff", "assistant engineer", "engineer", "senior engineer", "technique lead", "manger"]
        # if not in titles_list
        if title.lower() not in titles_list:
            # else raise and error message
            raise serializers.ValidationError(" title must be in any of these {}".format(titles_list))

        # gender for that employee
        gender = data["gender"]
        # gender list
        gender_list = ["M", "F"]
        # if not in gender_list
        if gender not in gender_list:
            # else raise and error message
            raise serializers.ValidationError(" gender must be in any of these {}".format(gender_list))

        return data
