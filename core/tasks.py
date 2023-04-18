from celery import shared_task

from django.contrib.auth import get_user_model
from core.models import Loan,Product
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
            guarantor_id1 = None
            guarantor_id2 = None
            
            if row.guarantor_id1 is not None:
                guarantor_id1 = row.guarantor_id1
                
            elif row.guarantor_id2 is not None:
                guarantor_id2 = row.guarantor_id2
            
            # timestamp_str = '1479340800000'
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
                # loan_date=datetime.datetime.fromisoformat(str(row.disbursement_date)),
                # start_date=datetime.datetime.fromisoformat(str(row.loan_start_date)),
                # end_date=datetime.datetime.fromisoformat(str(row.loan_end_date)),
                
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