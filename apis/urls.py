from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *

urlpatterns = [
    # prescription api
    path("prescriptions/", get_prescriptions, name="get_prescriptions"),
    path("prescriptions/add/", add_prescription, name="add_prescriptions"),
    path("prescriptions/update/<int:pk>/", update_prescription, name="update_prescription"),
    path("prescriptions/delete/<int:pk>/", delete_prescription, name="delete_prescription"),

    # token api
    path('token-auth/', obtain_auth_token, name='api_token_auth')
]