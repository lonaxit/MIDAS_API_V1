from django.urls import path,include
from cooperators.api.views import *


urlpatterns =[
     
    path('userbalances/<str:startdate>/<str:enddate>/',userLoanBalancesByDate.as_view(),name="user-balances"),
    path("myloans/", userLoans.as_view(), name="my-loans"),
    path('<str:startdate>/<str:enddate>/Depositstatement/',DepositStatement.as_view(),name="deposit-statement"),
 ]