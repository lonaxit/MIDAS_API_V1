from celery import shared_task

from django.contrib.auth import get_user_model
from core.models import Loan,Product,Deduction
from django.db import transaction
from rest_framework.exceptions import ValidationError
import math
import io, csv, pandas as pd
import json
import datetime
User = get_user_model()

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task
def mul(x, y,z):
    print( x * y * z)
    
@shared_task
def create_loan_subscription(data):
    # data = json.loads(data)
    
    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    try:
        for row in data_frame.itertuples():
            guarantor_id1 = 0
            guarantor_id2 = 0
            
            if pd.isnull(row.guarantor_id1):
                # Do something if the cell is empty
                pass
            else:
                guarantor_id1 = row.guarantor_id1
                
            if pd.isnull(row.guarantor_id2):
                # Do something if the cell is empty
                pass
            else:
                guarantor_id2 = row.guarantor_id2
                
            loan_date_stamp=row.disbursement_date
            loan_date_timestamp_ms = int(loan_date_stamp) / 1000
            loan_date = datetime.datetime.utcfromtimestamp(loan_date_timestamp_ms)
            
            start_date_stamp=row.loan_start_date
            start_date_timestamp_ms = int(start_date_stamp) / 1000
            start_date = datetime.datetime.utcfromtimestamp(start_date_timestamp_ms)
            
            end_date_stamp=row.loan_end_date
            end_date_timestamp_ms = int(end_date_stamp) / 1000
            end_date = datetime.datetime.utcfromtimestamp(end_date_timestamp_ms)
           
            Loan.objects.create(
                loan_date=loan_date,
                start_date=start_date,
                end_date=end_date,
               
                active=row.loan_status,
                transaction_code=row.ref.replace('-', ''), 
                sub_id=row.id,
                applied_amount=row.amount_applied,
                approved_amount=row.amount_approved,
                monthly_deduction=row.monthly_deduction,
                net_pay=0.0,
                tenor=row.custom_tenor,
                created_by=User.objects.get(pk=1),
                product=Product.objects.get(pk=row.product_id),
                owner=User.objects.get(pk=row.user_id),
                guarantor_one=guarantor_id1,
                guarantor_two=guarantor_id2,
            )
                  
    except ValueError as e:
        raise ValueError(f"Invalid value: {e}")
    except TypeError as e:
        raise TypeError(f"Type error: {e}")
    
    
@shared_task
def upload_loan_deduction(data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    try:
        for row in data_frame.itertuples():
            amount_deducted = None
            amount_debited = None
            
            if pd.isnull(row.amount_deducted):
                # Do something if the cell is empty
                pass
            else:
                amount_deducted = row.amount_deducted
                
            if pd.isnull(row.amount_debited):
                # Do something if the cell is empty
                pass
            else:
                amount_debited = row.amount_debited
                
            _date_stamp=row.entry_month
            _date_timestamp_ms = int(_date_stamp) / 1000
            _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
            
            Deduction.objects.create(
                loanee=User.objects.get(pk=row.user_id),
                loan=Loan.objects.get(pk=1),
                credit = amount_deducted,
                debit = amount_debited,
                narration = row.notes,
                transaction_code=row.deduction_reference.replace('-', ''), 
                transaction_date=_date,
                deduction_sub_id=row.lsubscription_id,
                created_by=User.objects.get(pk=1),
            )
                  
    except ValueError as e:
        raise ValueError(f"Invalid value: {e}")
    except TypeError as e:
        raise TypeError(f"Type error: {e}")