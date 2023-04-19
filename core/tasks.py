from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.contrib.auth import get_user_model
from core.models import Loan,Deduction
from django.db import transaction
User = get_user_model()
from rest_framework.exceptions import ValidationError
import math
import io, csv, pandas as pd
import json

# from midas.celery import app

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task
def mul(x, y):
    print( x * y)   
    

# @app.task
@shared_task
def create_loan_subscription(data):
    # data = json.loads(data)
    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    print(data_frame)
    print(3 * 7)
    
@shared_task
def upload_loan_deduction(data):
    # data = json.loads(data)
    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    print(data_frame)
    print(3 * 7)
   
   
# update loan deduction swith correct loan ids
@shared_task
def update_loan_deduction_loanids():
    """
    Update the 'loan' field of all deductions based on the related loan subscription ID.

    This function loops through all loans, filters deductions based on their
    subscription ID, and updates their 'loan' field to match the corresponding
    loan's ID.
    """
    loans = Loan.objects.all()

    with transaction.atomic():
        for loan in loans:
            deductions = Deduction.objects.filter(deduction_sub_id=loan.sub_id)

            if deductions.exists():
                deductions.update(loan=loan.id)
            else:
                # If there are no deductions for this loan, do nothing
                pass

