from celery import shared_task
from core.models import *
from django.db import transaction
User = get_user_model()
from rest_framework.exceptions import ValidationError
import math

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"

@shared_task
def mul(x, y):
    return x * y

@shared_task
def create_loan_subscription(dtframe,request):
    
    try:
                 
        for dtframe in dtframe.itertuples():
            guarantor_id1 = 0
            guarantor_id2 = 0
                    
            if not math.isnan(dtframe.guarantor_id1):
                
                guarantor_id1 = dtframe.guarantor_id1
                
            elif not math.isnan(dtframe.guarantor_id2):
                
                guarantor_id2 = dtframe.guarantor_id2
                    
            Loan.objects.create(
                        loan_date = dtframe.disbursement_date,
                        start_date = dtframe.loan_start_date,
                        end_date = dtframe.loan_end_date,
                        active = dtframe.loan_status,
                        transaction_code = dtframe.ref.replace('-', ''), 
                        sub_id = int(dtframe.id),
                        applied_amount= float(dtframe.amount_applied),
                        approved_amount = float(dtframe.amount_approved),
                        monthly_deduction = float(dtframe.monthly_deduction),
                        net_pay= float(0.00),
                        tenor = int(dtframe.custom_tenor),
                        created_by = request.user,
                        product= Product.objects.get(pk=int(dtframe.product_id)),
                        owner = User.objects.get(pk = int(dtframe.user_id)),
                        guarantor_one= guarantor_id1,
                        guarantor_two = guarantor_id2,
                    )
                  
    except Exception as e:
        
        raise ValidationError(e)