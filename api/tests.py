from django.urls import reverse
from django.test import TestCase, Client

# REST imports
from rest_framework import status
from rest_framework.test import APITestCase

# other imports
import datetime

# local imports
from api.models import *


# POST API upload_price Test
class Test_A_EmployeeHireAPI(APITestCase):

    # initialize inputs
    def setUp(self):

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

        # obtain each date and price in list
        for key in data.keys():

            # insert into database
            d = Departments(dept_no   = key,
                            dept_name = data[key],
                            )
            # saving assigined data
            d.save()

        self.valid_input = {
                        	"birth_date": "1994-01-01",
                        	"employee_id": 1,
                        	"first_name": "shinto",
                        	"last_name": "joseph",
                        	"gender": "M",
                        	"salary": ["2015-01-01", "2016-01-01"],
                        	"department": "Customer Service",
                        	"title": "staff",
                        	"hire_date": "2015-01-01"
                        }

    def test_valid_upload(self):

        # structure of the output data
        output_data = [{
                    	"status": True,
                    	"data": {
                    		"message": "Data successfully ingested"
                    	}
                    }]

        # url to be tested
        url = reverse('employee_hire')

        # Obtaining the POST response for the input data
        response = self.client.post(url, self.valid_input, format='json')

        # checking weather the outputa data is as per the requirement
        self.assertEqual(response.data, output_data)

        # checking wether the response is success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
