from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *

urlpatterns = [
    # prescription api
    path("prescriptions/", get_prescriptions, name="get_prescriptions"),
    path("prescriptions/add/", add_prescription, name="add_prescriptions"),
    path("prescriptions/update/<int:pk>/", update_prescription, name="update_prescription"),
    path("prescriptions/delete/<int:pk>/", delete_prescription, name="delete_prescription"),

    # medications api
    # path("medications/", get_medications_by_date, name="get_medications_by_date"),
    # path("medications/add/", add_medication, name="add_medication"),

    # token api
    path('token-auth/', obtain_auth_token, name='api_token_auth')
]