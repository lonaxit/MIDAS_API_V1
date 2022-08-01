
import csv
import io
import random
import string

import openpyxl
import pandas as pd
from cooperators.api.serializers import *
from core.api.serializers import *
from core.api.permissions import *
# # import models
from core.models import *
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from requests import request
# # from rest_framework import mixins
from rest_framework import generics, status
# # import validation errors
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import *
# # import Response
from rest_framework.response import Response
# # import here below used for class based views
from rest_framework.views import APIView



# my loans
class userLoans(generics.ListAPIView):
    
    serializer_class = LoanSerializer
    permission_classes= [IsAuthenticated,IsLoanOwnerOnly]
    
    def get_queryset(self):
        
        
        user = self.request.user
        Loans = Loan.objects.filter(owner=user)
        if Loans: 
            return Loans
        raise ValidationError('No Loans Available Yet!')


# List user cumulative loan balances by date
class userLoanBalancesByDate(generics.ListAPIView):
    
    serializer_class = UserCumulativeBalancesSerializer
    permission_classes= [IsAuthenticated]
    
    def get_queryset(self):
        
        user = self.request.user
        
        return Loan.objects.filter(owner=user).distinct('owner')
       
    
    def get_serializer_context(self):
        startDate = self.kwargs.get('startdate')
        endDate = self.kwargs.get('enddate')
        
        context = {'startdate':startDate,'enddate':endDate}
        
        return context
    
# my loans 
# class loanHistory(generics.RetrieveAPIView):
  
#     serializer_class = loanHistorySerializer
#     permission_classes= [IsAuthenticated,IsLoanOwnerOrStaff]
    
#     def get_queryset(self):
#         # user = self.request.user
#         return Loan.objects.all()
