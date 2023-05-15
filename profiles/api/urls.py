from django.urls import path,include

from profiles.api.views import *

urlpatterns =[
    
    path("<int:pk>/profileupdate/", ProfileRetrieveUpdate.as_view(), name="update-profile"),
    path("list-profile/", GetProfileList.as_view(), name="list-profile"),
    path('<int:user>/profile/',GetProfile.as_view(),name='profile'),
    path('<int:user>/my-profile/',GetProfileMobile.as_view(),name='my-profile'),
    path('user/profile/',UserProfileView.as_view(),name='user-profile'),

]