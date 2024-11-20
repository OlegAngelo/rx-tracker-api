from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import * 

urlpatterns = [
    path("medications/", get_medications, name="get_medication"),
    path("medications/add/", add_medication, name="add_medication"),
    path('token-auth/', obtain_auth_token, name='api_token_auth')
]
