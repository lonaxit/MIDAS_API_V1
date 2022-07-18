
import random
import string

import io, csv, pandas as pd
from core.api.serializers import *
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
    permission_classes =[IsAuthenticated]



class ProductSchemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =ProductScheme.objects.all()
    serializer_class = ProductSchemeSerializer
    permission_classes =[IsAuthenticated]
    
    
    
# List all products
class ProductList(generics.ListAPIView):
    queryset =Product.objects.all()
    serializer_class= ProductSerializer
    permission_classes =[IsAuthenticated]
    

# create product
class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes= [IsAuthenticated]
    
    def perform_create(self,serializer):
        scheme_pk = self.kwargs.get('pk')
        
         
        # get the Scheme
        # productScheme = ProductScheme.objects.get(pk=scheme_pk)
        
        
        productScheme = get_object_or_404(ProductScheme, pk=scheme_pk)
        
       
        # _user = self.request.user
    
        serializer.save(product_scheme=productScheme)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=[IsAuthenticated]



class LoanUpload(generics.CreateAPIView):
    serializer_class = LoanSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated]
    
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
            
            print(dtframe.monthly_deduction.sum())

            # TODO Save total sum of deductions in a summary table
            
            # generate random number 
            random_number = ''.join((random.choice(string.digits) for x in range(10)))
          
            for dtframe in dtframe.itertuples():
                
                
                loanObj = Loan.objects.create(
                                    owner=User.objects.get(pk=dtframe.owner),
                                    product=Product.objects.get(pk=dtframe.product),
                                    transaction_code = random_number,
                                    applied_amount=dtframe.applied_amount,
                                    loan_date = dtframe.loan_date,
                                    start_date=dtframe.start_date,
                                    end_date = dtframe.end_date,
                                    approved_amount=dtframe.approved_amount,
                                    monthly_deduction=dtframe.monthly_deduction,
                                    net_pay=dtframe.net_pay,
                                    tenor=dtframe.tenor,
                                    created_by=User.objects.get(pk=dtframe.created_by),
                                    )
           
        return Response(
                {'msg':'Loan(s) created successfuly'},
                status = status.HTTP_201_CREATED
                )


class LoanListCreate(generics.ListCreateAPIView):
    
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes =[IsAuthenticated]
    

class LoanDetail(generics.RetrieveUpdateDestroyAPIView):
    
    # allow get, put and destroy methods
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    
    # permission_classes = [IsReviewUserOrReadOnly]
    
#     # throttle_classes =[UserRateThrottle,AnonRateThrottle]
    
#     # using ScopedRateThrottle
#     # throttle_classes =[ScopedRateThrottle]
#     # throttle_scope = 'review-detail'
# 


# List all loans given a product id

class LoansByProduct(generics.ListAPIView):
  
    serializer_class = LoanSerializer
    permission_classes =[IsAuthenticated]
  
    
    # over writing default queryset 
    def get_queryset(self):
        # get the wachlist pk
        pk = self.kwargs['pk']
        return Loan.objects.filter(product=pk)




class MonthlyLoanDeductionUpload(generics.CreateAPIView):
    serializer_class = MasterLoanDeductionUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsAuthenticated]
    
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
            
            total_cumulative = dtframe.AMOUNT.sum()
           

            # TODO Save total sum of deductions in a summary table
            
            # generate random number 
            random_number = ''.join((random.choice(string.digits) for x in range(10)))
            
          
            for dtframe in dtframe.itertuples():
                
                
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
                                    created_by=request.user,
                                    )
        return Response(
                {'msg':'Records created successfuly'},
                status = status.HTTP_201_CREATED
                )


# list cumulative monthly loan deduction
class ListMonthlySummary(generics.ListAPIView):
    serializer_class = MasterLoanDeductionSummarySerializer
    queryset = MasterLoanDeductionSummary.objects.all()
    permission_classes =[IsAuthenticated]
    
# individual loan deduction
class DeductionsList(generics.ListAPIView):
    serializer_class = DeductionSerializer
    queryset = Deduction.objects.all()
    # permission_classes =[IsAuthenticated]  
    
    
    
# Create a deduction given a pk from a master deduction table
class CreateBulkLoanDeduction(generics.CreateAPIView):
    
    serializer_class = DeductionSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes=[ReviewCreateThrottle]
    
    def get_queryset(self):
        return Deduction.objects.all()
     
    #  we need to overwrite the current function becos we need to pass MasterLoanDeduction ID for which deduction is being created
    
    def perform_create(self,serializer):
        
        # pk = self.kwargs.get('pk')
        
        # get all active master deduction records
        masterDeductions= MasterLoanDeduction.objects.filter(active=True)
        
        if masterDeductions.exists():
            
            for master in masterDeductions:
                # 1. Get the user using the IPPIS NUMBER
                # 2. Next get the acctive loans of the user and distribute accordingly
                pass
        else:
            raise ValidationError('No unprocessed deductions yet!')
        
        # TODO
        # 1. Get IPPIS NUMBER
        # 2. USE THE IPPIS TO GET USER PROFILE FROM PROFILE TABLE
        # 3. USE THE USER ID (PK) TO GET A LIST OF ACTIVE LOANS FOR THE USER
        # 4. Check if only one loan exist, then just deduct everything
        # 5. Else iterate over the loans and get the loan balance for each loan
        
        # logic to prevent multple creation of reviews by a user
        # review_user = self.request.user
        # review_queryset = Review.objects.filter(watchlist=movie,review_user=review_user)
        # if review_queryset.exists():
            
        #     raise ValidationError("You have already reviewed this watchlist")
        
        # custom calculations
        # check if rating is 0 
        # if movie.number_rating == 0:
        #     movie.avg_rating = serializer.validated_data['rating']
        # else:
        #     movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
        # # increase the rating  
        # movie.number_rating = movie.number_rating + 1
        
        # # save
        # movie.save()
        
        # # save together with related watchlist and user
        # serializer.save(watchlist=movie,review_user=review_user)




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
