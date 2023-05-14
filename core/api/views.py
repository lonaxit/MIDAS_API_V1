
import random
import string
import math
import json
import io, csv, pandas as pd
from users.serializers import *
from core.api.serializers import *
from profiles.api.serializers import *
from core.api.permissions import *
from core.api.utilities import *
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
from core.tasks import create_loan_subscription, upload_loan_deduction,update_loan_deduction_loanids,upload_user_savings,update_profile,update_nok,update_bank,upload_master_loan_deduction,upload_master_saving

User = get_user_model()



class ProductSchemeListCreate(generics.ListCreateAPIView):
    # ListCreateAPIView gives us both the get and post methods
    queryset = ProductScheme.objects.all()
    serializer_class = ProductSchemeSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]



class ProductSchemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =ProductScheme.objects.all()
    serializer_class = ProductSchemeSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    # ========================
class ProductListCreate(generics.ListCreateAPIView):
        
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated,IsAuthOrReadOnly]
    

    
    # =========================
    
# List all products
class ProductList(generics.ListAPIView):
    queryset =Product.objects.all()
    serializer_class= ProductSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

# create product
# class ProductCreate(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes= [IsAuthenticated & IsAuthOrReadOnly]
    
#     def perform_create(self,serializer):
#         scheme_pk = self.kwargs.get('pk')
        
#         # get the Scheme
#         # productScheme = ProductScheme.objects.get(pk=scheme_pk)

#         productScheme = get_object_or_404(ProductScheme, pk=scheme_pk)
        
#         # _user = self.request.user
    
#         serializer.save(product_scheme=productScheme)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly]



class LoanUpload(generics.CreateAPIView):
    serializer_class = LoanSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Loan.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        with transaction.atomic():
            # TODO
            # 1 CREATE EACH LOAN IN THE LOAN MODEL
            # 2. CREATE CORRESPONDING LOAN IN THE CONSOLIDATED LOANS TABLE AS DEBIT
            
            # generate random number 
            random_number = ''.join((random.choice(string.digits) for x in range(10)))
            
            try:
                
                for dtframe in dtframe.itertuples():
                    
                    
                    loanObj = Loan.objects.create(
                                    owner=User.objects.get(pk=dtframe.owner),
                                    product=Product.objects.get(pk=dtframe.product),
                                    transaction_code = random_number,
                                    applied_amount=int(dtframe.applied_amount),
                                    loan_date = dtframe.loan_date,
                                    start_date=dtframe.start_date,
                                    end_date = dtframe.end_date,
                                    approved_amount=int(dtframe.approved_amount),
                                    monthly_deduction=int(dtframe.monthly_deduction),
                                    net_pay=int(dtframe.net_pay),
                                    tenor=int(dtframe.tenor),
                                    created_by=User.objects.get(pk=dtframe.created_by),
                                    )
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Loan(s) created successfuly'},
                status = status.HTTP_201_CREATED
                )

# List all loans in the system
class LoanListCreate(generics.ListCreateAPIView):
    
    queryset = Loan.objects.all().order_by('owner')
    serializer_class = LoanListCreateSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    def perform_create(self,serializer):
        
        createdBy = self.request.user
        serializer.save(created_by=createdBy)
        
    

# create a loan given a user ID
class LoanCreate(generics.CreateAPIView):
    
    """
    Create a Loan given a user id
   
    """

    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    

    def get_queryset(self):
        return Loan.objects.all()
    
    def perform_create(serializer,self, request,):
        
        pk = self.kwargs.get('int')
        try:
             userObj = User.objects.get(pk=pk)
             action_by = request.user
             
             serializer.save(owner=userObj,created_by=action_by)
             
        except User.DoesNotExist:
            
            raise ValidationError('This user does not exist!')
        
     # works as well
     
# class LoansByUser(APIView):
#     queryset = Loan.objects.all()  
#     serializer_class = LoanSerializer
#     permission_classes =[IsAuthenticated]
#     lookup_field ='owner'
    
    
#     def get(self,request,*args,**kwargs):
        
#         user_pk = self.kwargs['pk']
#         try:
#             user = User.objects.get(pk=user_pk)
#             Loans = Loan.objects.filter(owner=user)
            
#             if not Loans:
#                 return Response({'Error': 'User Not Found!'},
#                     status=status.HTTP_404_NOT_FOUND)
#             return Response(list(Loans.values()))
        
#         except User.DoesNotExist:
            
#             return Response({'Error': 'User Not Found!'},
#                     status=status.HTTP_404_NOT_FOUND)




    
   


# list loans by an individual user
class LoansByUser(generics.ListAPIView):
    """
    List Method

    Parameters:
        user id

    Returns:
        A list of loans for user
    """
      
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    lookup_field ='owner'
    
    # over writing default queryset 
    def get_queryset(self):
        # get the wachlist pk
        user_pk = self.kwargs['pk']
        # try:
            # user = User.objects.get(pk=user_pk)
        Loans = Loan.objects.filter(owner=user_pk)
            
            # if not Loans:
            #     raise ValidationError('No Loans For This User')
        return Loans
        
        # except User.DoesNotExist:
            
            # get_queryset shoud not return a response
            # return Response({'Error': 'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
            # raise ValidationError('User Does Not exist')
       
        
    

# get detail of a specific loan
class LoanDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of a  loan using loan id

    """
    
    queryset = Loan.objects.all()
    serializer_class = LoanDetailSerializer
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
#     # throttle_classes =[UserRateThrottle,AnonRateThrottle]
    
#     # using ScopedRateThrottle
#     # throttle_classes =[ScopedRateThrottle]
#     # throttle_scope = 'review-detail'
# 


# List all loans given a product id

class LoansByProduct(generics.ListAPIView):
  
    serializer_class = LoanSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
  
    
    # over writing default queryset 
    def get_queryset(self):
      
        pk = self.kwargs['pk']
        loans = Loan.objects.filter(product=pk)
        
        if loans:
            return loans
        raise ValidationError('No Loans For This Product')
      

class MonthlyLoanDeductionUpload(generics.CreateAPIView):
    serializer_class = MasterLoanDeductionUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return MasterLoanDeduction.objects.all()
    
    def post(self, request, *args, **kwargs):
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        with transaction.atomic():
            # TODO
            # 1 CREATE EACH LOAN IN THE LOAN MODEL
            # 2. CREATE CORRESPONDING LOAN IN THE CONSOLIDATED LOANS TABLE AS DEBIT
            try:
                
                total_cumulative = dtframe.AMOUNT.sum()
        
                
                # generate random number 
                random_number = ''.join((random.choice(string.digits) for x in range(10)))
                
            
                for dtframe in dtframe.itertuples():
                    
                    transaction_date = dtframe.DATE
                    
                    loanObj = MasterLoanDeduction.objects.create(  
                                        name= dtframe.NAME,
                                        ippis_number = dtframe.IPPIS_NUMBER,
                                        narration = dtframe.NARRATION,
                                        entry_date = dtframe.DATE,
                                        transaction_code = random_number,
                                        cumulative_amount = dtframe.AMOUNT,
                                        created_by=request.user,
                                        )


                # save in the monthly loan summary deduction table
                # TODO REMOVE FOR NOW
                # MasterLoanDeductionSummary.objects.create(
                #                         transaction_code = random_number,
                #                         monthly_cumulative = float(total_cumulative),
                #                         transaction_date =transaction_date,
                #                         created_by=request.user,
                #                         )
            except Exception as e:
                # raise ValidationError('A bad operation happened!')
                return Response(
                {'msg':'Soemthing unexpected happened'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            
        return Response(
                {'msg':'Records created successfuly'},
                status = status.HTTP_201_CREATED
                )


# update Master Loan Deductions
class MasterDeductionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MasterLoanDeduction.objects.all()
    serializer_class = MonthlyLoanDeductionSerializer
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly]
    
# list all Master Deduction
class ListMasterDeduction(generics.ListAPIView):
    queryset = MasterLoanDeduction.objects.all().order_by('entry_date')
    serializer_class = MonthlyLoanDeductionSerializer
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly]


# list cumulative monthly loan deduction
class ListMonthlySummary(generics.ListAPIView):
    serializer_class = MasterLoanDeductionSummarySerializer
    queryset = MasterLoanDeductionSummary.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
# list loan deductions
class DeductionsList(generics.ListAPIView):
    serializer_class = DeductionSerializer
    queryset = Deduction.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly] 
    


class DeductionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly] 
    

# Create bulk deduction from a master deduction table
class CreateBulkLoanDeduction(generics.CreateAPIView):
    
    serializer_class = DeductionSerializer
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    # throttle_classes=[ReviewCreateThrottle]
    
    def get_queryset(self):
        return Deduction.objects.all()
     
    #  we need to overwrite the current function becos we need to pass MasterLoanDeduction ID for which deduction is being created
    
    def post(self,request,*args, **kwargs):
        
        # pk = self.kwargs.get('pk')
        
        # get all active master deduction records
        masterDeductions= MasterLoanDeduction.objects.filter(active=True)
        
        # get all active loans
       
        activeLoans = Loan.objects.filter(active=True)
        
        allDeductions = Deduction.objects.filter(loan__active=True)
        
        if masterDeductions.exists():
           
            for master in masterDeductions:
                
                try:
                    
                    ippis_Deduction = master.cumulative_amount
                    
                    profile = Profile.objects.get(ippis=master.ippis_number)
                    
                    # get all active loans for a user
                    myLoans = activeLoans.filter(owner=profile.user)
                    
                    # total Monthly Deduction
                    total_MonthlyDedcution = activeLoans.aggregate(totalMonthlyDeduction=Sum('monthly_deduction'))
                    
                    monthlyDeduction = total_MonthlyDedcution['totalMonthlyDeduction']
                    
                    
                    if ippis_Deduction > monthlyDeduction:
                        continue
                    
                    
                    userDeductions = allDeductions.filter(loanee=profile.user)
                    
                
                    for singleLoan in myLoans:
               
                        # get principal loan amount
                        loanPrincipal  = singleLoan.approved_amount
                           
                        totalcredit = userDeductions.filter(loan=singleLoan).aggregate(credit=Sum('credit'))
                        
                        totaldebit = userDeductions.filter(loan=singleLoan).aggregate(debit=Sum('debit'))
                        
                        credits = totalcredit['credit']
                        debits = totaldebit['debit']
                        
                        if not credits:
                            credits =0
                        if not debits:
                            debits =0
                            
                        payments = credits-debits
                        
                        # balance
                        bal = loanPrincipal-payments
                        
                        if(bal and bal <= singleLoan.monthly_deduction):
                            ippis_Deduction = ippis_Deduction-bal
                            
                            Deduction.objects.create(  
                                    loanee=profile.user,
                                    loan= singleLoan,
                                    credit = bal,
                                    narration = master.narration,
                                    transaction_date = master.entry_date,
                                    transaction_code = master.transaction_code,
                                    created_by=request.user,
                                    )
                            deactivateLoan(singleLoan)
                            
                           
                            
                        elif(bal and bal > ippis_Deduction):
                            ippis_Deduction = ippis_Deduction-singleLoan.monthly_deduction
                          
                            Deduction.objects.create(  
                                    loanee=profile.user,
                                    loan= singleLoan,
                                    credit = singleLoan.monthly_deduction,
                                    narration = master.narration,
                                    transaction_date = master.entry_date,
                                    transaction_code = master.transaction_code,
                                    created_by=request.user,
                                    )
                            deactivateLoan(singleLoan)
                         
                        elif(ippis_Deduction > bal):
                           continue
                        
                        
                    # update the master record to inactive
                    master.active = False
                    master.save()
                            
               
                    
                # except Profile.DoesNotExist:
                #     continue
                except Profile.DoesNotExist:
                    continue
                
            return Response(
                {'msg':'Loan deductions created successfully'},
                status = status.HTTP_201_CREATED
                )
        else:
            raise ValidationError('No unprocessed deductions yet!')
        
        
class DeductionCreate(generics.CreateAPIView):
    
    """
    Create a deduction given a loan id
   
    """

    serializer_class = DeductionSerializer
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    

    def get_queryset(self):
        return Deduction.objects.all()
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('loan_pk')
        try:
             loanObj = Loan.objects.get(pk=pk)
             user = loanObj.owner
             
             serializer.save(loanee=user,loan=loanObj,created_by=self.request.user)
             
        except Loan.DoesNotExist:
            
            raise ValidationError('No Loan Record Found!')



# get all loan balances by date
class ListBalances(generics.ListAPIView):
    
    serializer_class = AllLoanBalancesByDateSerializer
    permission_classes= [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
       return Loan.objects.filter(active=True).distinct('owner')
       
    
    def get_serializer_context(self):
        startDate = self.kwargs.get('startdate')
        endDate = self.kwargs.get('enddate')
        
        context = {'startdate':startDate,'enddate':endDate}
        
        return context
    
    
# STOPPED PERMISSION CHECK HERE, CONTINUE BELOW
# individual loan balance using Loan id
class IndividualLoanBalance(generics.RetrieveAPIView):
  
    serializer_class = IndividualLoanBalanceSerializer
    permission_classes= [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
        return Loan.objects.all()
    

# loan statement using userid, startdate and end date
class LoanStatement(generics.ListAPIView):
    
    serializer_class = UserLoanStatementByDateSerializer
    permission_classes= [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
        user_id = self.kwargs.get('userid')
        
        try:
            user = User.objects.get(pk=user_id)
            userLoans = Loan.objects.filter(owner=user)
            
        except User.DoesNotExist:
            raise ValidationError('User Does Not Exist')   
        return userLoans
       
    
    def get_serializer_context(self):
        startDate = self.kwargs.get('startdate')
        endDate = self.kwargs.get('enddate')
        
        context = {'startdate':startDate,'enddate':endDate}
        
        return context

        
class MasterSavingUpload(generics.CreateAPIView):
    serializer_class = SavingMasterUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return SavingMaster.objects.all()
    
    def post(self, request, *args, **kwargs):
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        with transaction.atomic():
           
            try:
                
                total_cumulative = dtframe.AMOUNT.sum()
            

                
                # generate random number 
                random_number = ''.join((random.choice(string.digits) for x in range(10)))
                
            
                for dtframe in dtframe.itertuples():
                    
                    trans_date = dtframe.DATE
                    savingMasterObj = SavingMaster.objects.create(  
                                        name= dtframe.NAME,
                                        ippis_number = dtframe.IPPIS_NUMBER,
                                        narration = dtframe.DESCRIPTION,
                                        transaction_date = dtframe.DATE,
                                        transaction_code = random_number,
                                        amount = dtframe.CONTRIBUTION,
                                        upload_by=request.user,
                                        )

            
                # save in the monthly saving summary deduction table
                MasterSavingSummary.objects.create(
                                        transaction_code = random_number,
                                        transaction_date =trans_date,
                                        monthly_cumulative = float(total_cumulative),
                                        created_by=request.user,
                                        )
            except Exception as e:
                # raise ValidationError('Something bad happened')
                return Response(
                {'msg':'Something unexpected happened'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            
        return Response(
                {'msg':'Records created successfuly'},
                status = status.HTTP_201_CREATED
                )

class ListMasterSaving(generics.ListAPIView):
    queryset = SavingMaster.objects.all().order_by('transaction_date')
    serializer_class = SavingMasterSerializer
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly]

# Manage Master Savings
class MasterSavingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavingMaster.objects.all()
    serializer_class = SavingMasterSerializer
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly]


# Create bulk saving deduction from a master saving deduction table
class CreateBulkSaving(generics.CreateAPIView):
    
    serializer_class = SavingSerializer
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    # throttle_classes=[ReviewCreateThrottle]
    
    def get_queryset(self):
        return SavingMaster.objects.all()
     
    #  we need to overwrite the current function becos we need to pass MasterLoanDeduction ID for which deduction is being created
    
    def post(self,request,*args, **kwargs):
        
        # get all active master deduction records
        masterSaving= SavingMaster.objects.filter(active=True)
     
        if masterSaving.exists():
           
            for master in masterSaving:
                
                try:
                    
                    user = User.objects.get(ippis_number=master.ippis_number)
                            
                    Saving.objects.create(  
                        user=user,
                        credit = master.amount,
                        narration = master.narration,
                        transaction_date = master.transaction_date,
                        transaction_code = master.transaction_code,
                        created_by=request.user,
                        )  
                    master.active = False
                    master.save()
    
                except User.DoesNotExist:
                    continue
                
            return Response(
                {'msg':'savings created successfully'},
                status = status.HTTP_201_CREATED
                )
        else:
            raise ValidationError('No unprocessed savings yet!')

# saving list
class SavingsList(generics.ListAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
# All deposit for a logged in user

# saving list
class myDepositList(generics.ListAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.filter()
    permission_classes =[IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        return Saving.objects.filter(user=user)


class SavingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]


# create  saving Manually given a user id
class CreateSaving(generics.CreateAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    def perform_create(self, serializer):
        
        user_id = self.kwargs.get('userid')
        
        try:
            user = User.objects.get(pk=user_id)
            serializer.save(user=user,created_by=self.request.user)
        except User.DoesNotExist:
            raise ValidationError('No user exist!')
  
  
class ListUserSavings(generics.ListAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    lookup_field ='user'
    
    def get_queryset(self):
        
        pk = self.kwargs['pk']
        try:
            user = User.objects.get(pk=pk)
            Savings = Saving.objects.filter(user=user)
            
            if not Savings:
                raise ValidationError('No Saving(s) For This User')
            return Savings
        
        except User.DoesNotExist:          

            # get_queryset shoud not return a response
            # return Response({'Error': 'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
            raise ValidationError('User Does Not exist')
        
  
#  find statement of saving given a user id and date range start and end dates 
class StatementofSavings(generics.ListAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
        pk = self.kwargs['pk']
        start = self.kwargs['startdate']
        end = self.kwargs['enddate']
        try:
            user = User.objects.get(pk=pk)
            Savings = Saving.objects.filter(user=user,transaction_date__gte=start,transaction_date__lte=end)
            
            if not Savings:
                raise ValidationError('No savings or search criteria not fulfilled')
            return Savings
        
        except User.DoesNotExist:          

            raise ValidationError('User Does Not exist')

# find saving opening balance for user by date

class UserOpeningBalance(generics.RetrieveAPIView):
    
    serializer_class = UserOpeningBalanceSerializer
    permission_classes= [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        
       return User.objects.all()
       
    
    def get_serializer_context(self):
        startDate = self.kwargs.get('startdate')
        
        context = {'startdate':startDate}
        
        return context
    
  
        

#  find statement of saving date range start and end dates 
class allStatementByDate(generics.ListAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    # lookup_field ='user'
    
    def get_queryset(self):
        
        start = self.kwargs['startdate']
        end = self.kwargs['enddate']
        try:
          
            Savings = Saving.objects.filter(transaction_date__gte=start,transaction_date__lte=end)
            
            if not Savings:
                raise ValidationError('No saviongs or search criteria not fulfilled')
            return Savings
        
        except Exception as e:          

            raise ValidationError('User Does Not exist')
        

# data migration endpoints
class MigrateUsers(generics.CreateAPIView):
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return User.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        reader = reader.where(pd.notnull(reader), None)
        dtframe = reader
        
        with transaction.atomic():
              
            try:
                
                for dtframe in dtframe.itertuples():
                    
                    
                    userObj = User.objects.create(
                        username = int(dtframe.id),
                        first_name = dtframe.first_name,
                        last_name =  dtframe.last_name,
                        other_name =  dtframe.other_name,
                        ippis_number = int(dtframe.payment_number),
                        dob = dtframe.dob,
                        dofa = dtframe.dofa,
                        # password = set_password(dtframe.payment_number),
                        # date_joined = dtframe.date_entry,
                                    )
                    userObj.set_password(str(dtframe.payment_number))
                    userObj.date_joined = dtframe.date_entry
                    userObj.save()
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'User Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )

         
# migrate product categories 
class MigrateProductCategory(generics.CreateAPIView):
    serializer_class = ProductSchemeSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return ProductScheme.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        reader = reader.where(pd.notnull(reader), None)
        dtframe = reader
        
        with transaction.atomic():
              
            try:
                
                for dtframe in dtframe.itertuples():
                    
                    ProductScheme.objects.create(
                        name = dtframe.name,
                        description = dtframe.description,
                    )
                  
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Product Category Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )


# migrate products
class MigrateProducts(generics.CreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Product.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        reader = reader.where(pd.notnull(reader), None)
        dtframe = reader
        
        with transaction.atomic():
              
            try:
                
                for dtframe in dtframe.itertuples():
                    
                    Product.objects.create(
                        name = dtframe.name,
                        description = dtframe.description,
                        product_scheme= ProductScheme.objects.get(pk=int(dtframe.product_scheme))
                    )
                  
            except Exception as e:
                raise ValidationError(e)
           
        return Response(
                {'msg':'Products Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )

# migrate loan subscriptions
class MigrateLoanSub(generics.CreateAPIView):
    serializer_class = LoanSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Loan.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        reader = reader.where(pd.notnull(reader), None)
        dtframe = reader
        
        with transaction.atomic():
              
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
           
        return Response(
                {'msg':'Loans Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )
        
# Migrate loan subscription with celery
class loanMigrationCelery(generics.CreateAPIView):
    serializer_class = LoanSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Loan.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        # data = json.loads(json_data)

        
        with transaction.atomic():
            
            # data_frame = pd.read_json(json_data)
            # try:
            # print(json_data)
            # mul(5,10,2)
            create_loan_subscription.delay(json_data)
           
            # except Exception as e:
            #     raise ValidationError(e)
           
        return Response(
                {'msg':'Loans Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )


# migrate loan subscriptions without guarantors
class MigrateLoanDeductionCelery(generics.CreateAPIView):
    serializer_class = DeductionSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Deduction.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        
        
        with transaction.atomic():
              
            try:
                # call worker here
                upload_loan_deduction.delay(json_data)
                
            except Exception as e:
                raise ValidationError(e)
            except ValueError as e:
                raise ValueError(f"Invalid value: {e}")
            except TypeError as e:
                raise TypeError(f"Type error: {e}")
           
        return Response(
                {'msg':'Loans Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )     


# Migration: Update loan deduction ids

class MigrateUpdateDeductionIdsCelery(generics.GenericAPIView,):
    serializer_class = DeductionSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Deduction.objects.all()
    
    def post(self, request, *args, **kwargs):
        try:
            update_loan_deduction_loanids.delay()
        except Exception as e:
            raise ValidationError(e)

        return Response({'msg': 'Updated Successfully'}, status=status.HTTP_201_CREATED)


# celery upload user savings

class MigrateUserSavingCelery(generics.CreateAPIView):
    serializer_class = SavingSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Saving.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        
        
        with transaction.atomic():
              
            try:
                # call worker here
                userid = request.user.id
                upload_user_savings.delay(userid,json_data)
                
            except Exception as e:
                raise ValidationError(e)
        
           
        return Response(
                {'msg':'Loans Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                ) 
    
    
class MigrateProfileUpdateCelery(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Profile.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        try:
            update_profile.delay(json_data)
        except Exception as e:
            raise ValidationError(e)
                    
        return Response(
                {'msg':'Profile Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )
        
# update NOKS
class MigrateProfileNokCelery(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Profile.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        try:
            update_nok.delay(json_data)
        except Exception as e:
            raise ValidationError(e)
                    
        return Response(
                {'msg':'Nok Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )


# upate Banks
class MigrateProfileBanksCelery(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return Profile.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        try:
            update_bank.delay(json_data)
        except Exception as e:
            raise ValidationError(e)
                    
        return Response(
                {'msg':'Banks Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                )
        
#  migrate master loan deductions
class MigrateMasterLoanDeductionCelery(generics.CreateAPIView):
    serializer_class = MonthlyLoanDeductionSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return MasterLoanDeduction.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        try:
            userid = request.user.id
            upload_master_loan_deduction.delay(userid,json_data)
        except Exception as e:
            raise ValidationError(e)
                    
        return Response(
                {'msg':'Master Loan Deductions Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                ) 
      
        
#  migrate master saving deductions
class MigrateMasterSavingDeductionCelery(generics.CreateAPIView):
    serializer_class = SavingMasterSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated & IsAuthOrReadOnly]
    
    def get_queryset(self):
        # just return the review object
        return MasterLoanDeduction.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        data = request.FILES['file']
        reader = pd.read_excel(data)
        dtframe = reader
        
        json_data = dtframe.to_json()
        try:
            userid = request.user.id
            upload_master_saving.delay(userid,json_data)
        except Exception as e:
            raise ValidationError(e)
                    
        return Response(
                {'msg':'Master Deductions Migrated Successfuly'},
                status = status.HTTP_201_CREATED
                ) 



 
        
        

