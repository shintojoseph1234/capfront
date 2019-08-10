# Django imports
from django.shortcuts import render

# REST imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView

# local imports
from api.serializers import *
from api.models import (Employees, Departments, Dept_emp, Titles, Salaries)


# CONST: salary for each titles
salary_list = { "staff"                : "300000",
                "senior staff"         : "500000",
                "assistant engineer"   : "700000",
                "engineer"             : "900000",
                "senior engineer"      : "1200000",
                "technique lead"       : "2000000",
                "manger"               : "3000000"
            }

dept_list =  ["customer service",
             "sevelopment",
             "finance",
             "human resources",
             "human resources",
             "sales",
            ]

title_list = ["senior engineer",
             "staff",
             "engineer",
             "senior staff",
             "assistant engineer",
             "technique leader"
            ]

def get_error_message(error_type, message):
    '''
    Checks the error type and message,
    and returns error message with error code

    Parameters:
        error_type (str)    : The error type.
        message (dict)      : The response message from serializer.

    Returns:
        list: returns error message with error code
    '''

    if error_type == "DATA_ERROR":

        error_status = [{
                        "status": "error",
                        "data": {
                            "http_code": "400 BAD REQUEST",
                            "errors": [{
                                "error_code": 2000,
                                "error_message": message
                                }]
                            }
                        }]
        return Response(error_status, status=status.HTTP_400_BAD_REQUEST)

    else:
        error_status = [{
            "status": "error",
            "data": {
                "http_code": "500 INTERNAL SERVER ERROR",
                "errors": [{
                    "error_code": 2003,
                    "error_message": "Unknown Internal server error"
                    }]
                }
            }]

    return Response(error_status, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def populate_department_table(request):

    data = {
        	"d009": "Customer Service",
        	"d005": "Development",
        	"d002": "Finance",
        	"d003": "Human Resources",
        	"d001": "Marketing",
        	"d004": "Production",
        	"d006": "Quality Management",
        	"d008": "Research",
        	"d007": "Sales"
        }



    try:
        # obtain each date and price in list
        for key in data.keys():

            # insert into database
            d = Departments(dept_no   = key,
                            dept_name = data[key],
                            )
            # saving assigined data
            d.save()

        # response messages
        saved_status = True
        message = "Data successfully ingested"
        status_code = status.HTTP_201_CREATED

    except:
        # response messages
        saved_status = False
        message = "Failed to ingest data"
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


    # response
    success = [{
                "status": saved_status,
                "data": {
                        "message": message
                        }
               }]

    return Response(success, status=status_code)


class EmployeeHireViewSet(GenericAPIView):
    """
    API endpoint where you can insert employee details into the database

    Parameters:
        employee_id (int)       : employee id.
        first_name (str)        : employee first name.
        last_name (str)         : employee last name.
        gender (str)            : employee gender.
        birth_date (date)       : employee date of birth.
        salary (list)           : [from_date, to_date]
        department (str)        : employee department.
        title (str)             : employee title.
        hire_date (date)        : employee hired date.


    Returns:
        list: returns a success or failure message

    Curl:
        curl -X POST -d '''{"birth_date": "1994-01-01",
                        	"employee_id": 1,
                        	"first_name": "shinto",
                        	"last_name": "joseph",
                        	"gender": "M",
                        	"salary": ["2015-01-01", "2016-01-01"],
                        	"department": "Customer Service",
                        	"title": "staff",
                        	"hire_date": "2015-01-01"
                        }''' -H "Content-Type: application/json" \
                          http://localhost:8000/api/employee_hire/
    """

    queryset = ''
    serializer_class = EmployeeHireSerializer

    def post(self, request, *args, **kwargs):

        # obtain the data
        data = request.data
        # check data with serializer
        serializer = EmployeeHireSerializer(data=data)
        # if serialiser not valid
        if not serializer.is_valid():
            # return error message
            return get_error_message("DATA_ERROR", str(serializer.errors))

        # inputs from API
        employee_id     = data['employee_id']
        birth_date      = data['birth_date']
        first_name      = data['first_name']
        last_name       = data['last_name']
        gender          = data['gender']
        hire_date       = data['hire_date']
        title           = data['title']
        department      = data['department']
        salary          = data['salary']

        try:
            # obtain from and to dates
            from_date   = salary[0]
            to_date     = salary[1]
            # check from_dateis less than to_date
            if from_date > to_date:
                # return error message
                return get_error_message("DATA_ERROR",
                                        "from_date must be less than to_date")
        except:
            # return error message
            return get_error_message("DATA_ERROR", "from_date/to_date missing")


        try:
            # find the employe salary
            employee_salary = salary_list[title.lower()]
            # Query the model
            department_obj = Departments.objects.get(dept_name=department)

            e, created = Employees.objects.update_or_create(
                                                emp_no= employee_id,
                                                birth_date  = birth_date,
                                                first_name  = first_name,
                                                last_name   = last_name,
                                                gender      = gender,
                                                hire_date   = hire_date
                                            )

            t, created = Titles.objects.update_or_create(
                                                emp_no      = e,
                                                title       = title,
                                                from_date   = from_date,
                                                to_date     = to_date,
                                            )

            d, created = Dept_emp.objects.update_or_create(
                                                emp_no      = e,
                                                dept_no     = department_obj,
                                                from_date   = from_date,
                                                to_date     = to_date,
                                            )


            s, created = Salaries.objects.update_or_create(
                                                emp_no      = e,
                                                salary      = employee_salary,
                                                from_date   = from_date,
                                                to_date     = to_date,
                                            )


            # response messages
            saved_status = True
            message = "Data successfully ingested"
            status_code = status.HTTP_201_CREATED

        except:
            # response messages
            saved_status = True
            message = "Failed to ingest data"
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        # response
        success = [{
                    "status": saved_status,
                    "data": {
                            "message": message
                            }
                   }]

        return Response(success, status=status_code)


@api_view(['GET'])
def hike_eligible(request, employee_id):
    '''
    API endpoint that returns a list of dictionary saying employee eligible for
    hike or not

    Parameters:
        employee_id (int)    : employee ID.

    Returns:
        list: returns a list of dictionary having keys hike and designation
        (designation only if hike is True)

    Curl:
        curl -X GET -H 'Content-Type: application/json' \
        http://localhost:8000/api/eligible_for_hike/1/
    '''

    # converting data into dictionary format to serialiser
    data = {"employee_id":employee_id}
    # check data with serializer
    serializer = HikeEligibleSerializer(data=data)
    # if serialiser not valid
    if not serializer.is_valid():
        # return error message
        return get_error_message("DATA_ERROR", str(serializer.errors))

    try:
        # Query the model
        emp_obj = Employees.objects.get(emp_no=employee_id)
    except:
        # if not details set as empty
        emp_obj = []


    if emp_obj:
        # depart_number of employee
        dept_no = Dept_emp.objects.filter(emp_no=emp_obj)\
                                    .values_list("dept_no")[0][0]
        # depart_name of employee
        dept_name = Departments.objects.filter(dept_no=dept_no)\
                                .values_list("dept_name")[0][0]


        # title of employee
        title = Titles.objects.get(emp_no=emp_obj).title
        # employee hired date
        hire_date = emp_obj.hire_date
        # employee gender
        gender = emp_obj.gender
        # date of birth of employee
        dob = emp_obj.birth_date
        # todays date
        today = date.today()
        # age of employee
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        # employee experience
        experience = today.year - hire_date.year - ((today.month, today.day) < (hire_date.month, hire_date.day))

        # set hike initially as false
        result_dict = {"hike": False}
        # if dept_name in dept_list and title in title_list
        if dept_name.lower() in dept_list and title.lower() in title_list:
            # if experience greater than one enter
            if  experience > 1 and age > 20:
                # if gender is male and title = technique leader
                if gender == "M" and title.lower() == "technique leader":
                    # no hike
                    result_dict = {"hike": False}
                else:
                    # hike
                    result_dict = {"hike": True, "designation": title}

    else:

        result_dict = {}

    success = [{
                "status": "success",
                "data": result_dict
                }]


    return Response(success, status=status.HTTP_200_OK)
