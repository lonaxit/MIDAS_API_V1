
import random
import string

import io, csv, pandas as pd
from core.api.serializers import *
from core.api.permissions import *
# # import models
from core.models import *
from django.contrib.auth import get_user_model
# from django.db.models import Q, Sum, Avg, Max, Min
from django.db import transaction
from django.shortcuts import get_object_or_404
# # from rest_framework import mixins
from rest_framework import generics, status
# # import validation errors
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import *
# # import Response
from rest_framework.response import Response
# # import here below used for class based views
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser,FormParser

import openpyxl



User = get_user_model()
# CUSTOM DEFINED METHODS
def deactivateLoan(loanObj):

  
    
      loanPrincipal  = loanObj.approved_amount
                        
      # get loan balance from balance 
                        
      totalcredit = Deduction.objects.filter(loan=loanObj).aggregate(credit=Sum('credit'))
                        
      totaldebit = Deduction.objects.filter(loan=loanObj).aggregate(debit=Sum('debit'))
                        
      credits = totalcredit['credit']
      debits = totaldebit['debit']
                        
      if not credits: 
          credits =0
      if not debits:
          debits =0
                            
      payments = credits-debits
                        
       # balance
      bal = loanPrincipal-payments
      
      if bal == 0:
          loanObj.active = True
          loanObj.save()

def checkDistributionPlan(masterIPPISObj):
    pass