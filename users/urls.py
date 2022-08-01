from django.urls import path
from .views import *

urlpatterns=[
    path('register/',RegistrationView.as_view()),
    path('me/',RetrieveUserView.as_view()),
    path('all/users/',retrieveAllUsers.as_view(), name="all-users"),
    path('<int:pk>/user-update/',UpdateUser.as_view(), name="update-user"),
    
    # change password using userid
    path('<int:pk>/update-password/',UpdateUserPassword.as_view(), name="update-password"),
    
    # Change password using username
    path('username-update-password/',UpdatePasswordUsername.as_view(), name="username-update-password"),     
]