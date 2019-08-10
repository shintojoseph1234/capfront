# Django imports
from django.urls import path
#
# # REST imports
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

# local imports
from api import views

urlpatterns = [

    # API doc
    path('', include_docs_urls(title='Employee API', public=True)),

    # scheme view
    path('schema/', get_schema_view(title="Employee API"), name="schema_view"),

    # POST upload_price
    path('employee_hire/', views.EmployeeHireViewSet.as_view(), name="employee_hire"),

    # GET average_price null for less than 3 prices
    path('eligible_for_hike/<str:employee_id>/', views.hike_eligible, name="eligible_for_hike"),

    # populate
    path('populate_department/', views.populate_department_table, name="populate_department"),


]
