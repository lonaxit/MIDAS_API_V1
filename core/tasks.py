from celery import shared_task
from core.models import *
from django.db import transaction
User = get_user_model()
from rest_framework.exceptions import ValidationError
import math
import io, csv, pandas as pd
import json

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task
def mul(x, y):
    print( x * y)

# @shared_task
# def create_loan_subscription(dtframe,request):
    
#     try:
                 
#         for dtframe in dtframe.itertuples():
#             guarantor_id1 = 0
#             guarantor_id2 = 0
                    
#             if not math.isnan(dtframe.guarantor_id1):
                
#                 guarantor_id1 = dtframe.guarantor_id1
                
#             elif not math.isnan(dtframe.guarantor_id2):
                
#                 guarantor_id2 = dtframe.guarantor_id2
                    
#             Loan.objects.create(
#                         loan_date = dtframe.disbursement_date,
#                         start_date = dtframe.loan_start_date,
#                         end_date = dtframe.loan_end_date,
#                         active = dtframe.loan_status,
#                         transaction_code = dtframe.ref.replace('-', ''), 
#                         sub_id = int(dtframe.id),
#                         applied_amount= float(dtframe.amount_applied),
#                         approved_amount = float(dtframe.amount_approved),
#                         monthly_deduction = float(dtframe.monthly_deduction),
#                         net_pay= float(0.00),
#                         tenor = int(dtframe.custom_tenor),
#                         created_by = request.user,
#                         product= Product.objects.get(pk=int(dtframe.product_id)),
#                         owner = User.objects.get(pk = int(dtframe.user_id)),
#                         guarantor_one= guarantor_id1,
#                         guarantor_two = guarantor_id2,
#                     )
                  
#     except Exception as e:
        
#         raise ValidationError(e)
    
    
@shared_task
def create_loan_subscription(data):
    data = json.loads(data)

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(json.dumps(data))
    try:
        for row in data_frame.itertuples():
            guarantor_id1 = None
            guarantor_id2 = None
            
            if row.guarantor_id1 is not None:
                guarantor_id1 = row.guarantor_id1
                
            elif row.guarantor_id2 is not None:
                guarantor_id2 = row.guarantor_id2
                    
            Loan.objects.create(
                loan_date=row.disbursement_date,
                start_date=row.loan_start_date,
                end_date=row.loan_end_date,
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