from django.urls import path
from .views import *

urlpatterns=[
    path('register/',RegistrationView.as_view()),
    path('me/',RetrieveUserView.as_view()),
    path('all/users/',retrieveAllUsers.as_view(), name="all-users"),   
]