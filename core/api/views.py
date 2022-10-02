
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
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    
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
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
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
    serializer_class = LoanSerializer
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
                MasterLoanDeductionSummary.objects.create(
                                        transaction_code = random_number,
                                        monthly_cumulative = float(total_cumulative),
                                        transaction_date =transaction_date,
                                        created_by=request.user,
                                        )
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
        # activeLoans = Loan.objects.exclude(active=False)
        
        activeLoans = Loan.objects.filter(active=True)
        
        allDeductions = Deduction.objects.filter(loan__active=True)
        
        if masterDeductions.exists():
           
            for master in masterDeductions:
                
                try:
                    
                    profile = Profile.objects.get(ippis=master.ippis_number)
                    
                    # get all active loans for a user
                    myLoans = activeLoans.filter(owner=profile.user)
                    
                    # get total repayment
                    # sumRepayment = myLoans.aggregate(repayment=Sum('monthly_deduction'))
                    
                    # totalRepayment =sumRepayment['repayment']
                    
                    userDeductions = allDeductions.filter(loanee=profile.user)
                    
                    ippis_Deduction = master.cumulative_amount
                    
                    # no = 0
                    for singleLoan in myLoans:
                        # n=1
                        # get principal loan amount
                        loanPrincipal  = singleLoan.approved_amount
                        
                        # get loan balance from balance summary table
                        
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
                            # store the balance in loanbalance table
                            # Loanbalance.objects.create(  
                            #         loanee=profile.user,
                            #         loan= singleLoan,
                            #         current_blance = bal-bal,
                            #         narration = master.narration,
                            #         transaction_date = master.entry_date,
                            #         transaction_code = master.transaction_code,
                            #         created_by=request.user,
                            #         )
                            
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
                            # caculate the balance of the loan and store in loanbalance table
                        # elif(ippis_Deduction > bal):
                        #     continue
                        
                        
                    # update the master record to inactive
                    master.active = False
                    master.save()
                            
                            # n+=1
                    
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
                                        narration = dtframe.NARRATION,
                                        transaction_date = dtframe.DATE,
                                        transaction_code = random_number,
                                        amount = dtframe.AMOUNT,
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
                    
                    profile = Profile.objects.get(ippis=master.ippis_number)
                            
                    Saving.objects.create(  
                        user=profile.user,
                        credit = master.amount,
                        narration = master.narration,
                        transaction_date = master.transaction_date,
                        transaction_code = master.transaction_code,
                        created_by=request.user,
                        )  
                    master.active = False
                    master.save()
    
                except Profile.DoesNotExist:
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
        
        
          
# import io, csv, pandas as pd
# class UploadFileView(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         file = serializer.validated_data['file']
#         reader = pd.read_csv(file)
#         for _, row in reader.iterrows():
#             new_file = File(
#                        id = row['id'],
#                        staff_name= row["Staff Name"],
#                        position= row['Designated Position'],
#                        age= row["Age"],
#                        year_joined= row["Year Joined"]
#                        )
#             new_file.save()
#         return Response({"status": "success"},
#                         status.HTTP_201_CREATED)
