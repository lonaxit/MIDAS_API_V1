from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.contrib.auth import get_user_model
from core.models import Loan,Deduction,Saving,Profile,MasterLoanDeduction,SavingMaster
from django.db import transaction
User = get_user_model()
from rest_framework.exceptions import ValidationError
import math
import io, csv, pandas as pd
import json
import datetime

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
            
# upload user savings   
@shared_task
def upload_user_savings(request,data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
                credit_amt = None
                debit_amt = None
                
                if pd.isnull(row.amount_saved):
                    # Do something if the cell is empty
                    pass
                else:
                    credit_amt = row.amount_saved
                    
                if pd.isnull(row.amount_withdrawn):
                    # Do something if the cell is empty
                    pass
                else:
                    debit_amt = row.amount_withdrawn

                _date_stamp=row.entry_date
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                Saving.objects.create(
                    user=User.objects.get(pk=row.user_id),
                    credit = credit_amt,
                    debit = debit_amt,
                    transaction_code=row.ref_string.replace('-', ''), 
                    transaction_date=_date,
                    narration = row.notes,
                    created_by=request.user,
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")


@shared_task
def update_profile(data):
    """
    Update the 'profile' field of all users based on the related user ID.

    This function loops through all profiles, filters prodile based on their
    user ID, and updates relevant fields.
    """
    data_frame = pd.read_json(data)
    
    # profiles = Profile.objects.all()
    with transaction.atomic():
        for  row in data_frame.itertuples():
            
            try:
                # Attempt to get the order for the user
                profile= Profile.objects.get(user_id=row.id)
               
                # If the order exists, update it with the user's ID
                profile.staff_id = row.staff_no
                profile.home_address = row.home_add
                profile.email = row.email
                profile.employment_type = row.employ_type
                profile.gender = row.sex
                profile.job_cadre = row.job_cadre
                profile.marital_status = row.marital_status
                profile.phone = row.phone
                profile.dept = row.dept
                profile.title = row.title
                profile.member_type = row.membership_type
                profile.save()
            except Profile.DoesNotExist:
                pass
             

             
@shared_task
def update_nok(data):
    """
    Update the 'profile'  next of kin details.

    
    """
    data_frame = pd.read_json(data)
    
    # profiles = Profile.objects.all()
    with transaction.atomic():
        for  row in data_frame.itertuples():
            surname = row.first_name
            firstname = row.last_name
            othername = row.other_name
            
            full_name = surname + ' ' + firstname + ' ' + othername
            
            try:
                # Attempt to get the order for the user
                profile= Profile.objects.get(user_id=row.user_id)
                #update profile
                profile.nok_fullName = full_name
                profile.nok_relationship = row.relationship
                profile.nok_phone = row.phone
                profile.save()
            except Profile.DoesNotExist:
                pass
            
@shared_task
def update_bank(data):
    """
    Update the 'profile'  next of kin details.

    
    """
    data_frame = pd.read_json(data)
    
    # profiles = Profile.objects.all()
    with transaction.atomic():
        for  row in data_frame.itertuples():
          
            
            try:
                # Attempt to get the order for the user
                profile= Profile.objects.get(user_id=row.user_id)
                #update profile
                profile.bank = row.bank_name
                profile.bank_account = row.acct_number
                profile.save()
            except Profile.DoesNotExist:
                pass
            
@shared_task
def upload_master_loan_deduction(userid,data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    
    with transaction.atomic():
        try:
            for row in data_frame.itertuples():
            
                _date_stamp=row.entry_date
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                MasterLoanDeduction.objects.create(
                    name=row.name,
                    ippis_number=row.ippis_no,
                    cumulative_amount = row.cumulative_amount,
                    narration = row.description,
                    transaction_code=row.master_reference.replace('-', ''),
                    active = row.status, 
                    entry_date=_date,
                    created_by=User.objects.get(pk=userid),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")
        
        
# upload master savings 
@shared_task
def upload_master_saving(userid,data):

    # convert the JSON data to a DataFrame
    data_frame = pd.read_json(data)
    with transaction.atomic():
        
        try:
            for row in data_frame.itertuples():
            
                _date_stamp=row.entry_date
                _date_timestamp_ms = int(_date_stamp) / 1000
                _date = datetime.datetime.utcfromtimestamp(_date_timestamp_ms)
                
                SavingMaster.objects.create(
                    name=row.name,
                    ippis_number=row.ippis_no,
                    amount = row.saving_cumulative,
                    narration = row.notes,
                    transaction_code=row.ref_identification.replace('-', ''),
                    active = row.status, 
                    transaction_date=_date,
                    created_by=User.objects.get(pk=userid),
                )
                    
        except ValueError as e:
            raise ValueError(f"Invalid value: {e}")
        except TypeError as e:
            raise TypeError(f"Type error: {e}")