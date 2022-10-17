from django.urls import path,include

from core.api.views import *

urlpatterns =[
    
    path("schemes/", ProductSchemeListCreate.as_view(), name="schemes"),
    
    path("scheme-detail/<int:pk>/", ProductSchemeDetail.as_view(), name="scheme-detail"),
    
  
    path("products/",ProductListCreate.as_view(),name="products"),
    
    
    # path("product-list/", ProductList.as_view(), name="product-list"),
    # path("product-create/<int:pk>/", ProductCreate.as_view(), name="product-create"),
    
    path("product-detail/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    
    path('loan-upload/', LoanUpload.as_view(),name='loan-upload'),
    path('loans/', LoanListCreate.as_view(), name='loans'),
    path('loan-create/<int:pk>/', LoanCreate.as_view(), name='loan-create'),
    path('<int:pk>/loans/', LoansByUser.as_view(), name='user-loans'),
    path('loan/<int:pk>/', LoanDetail.as_view(), name='loan-detail'),
    path('product/<int:pk>/loans/', LoansByProduct.as_view(), name="product-loans"),
    
    
    path('masterdeduction/upload/',MonthlyLoanDeductionUpload.as_view(), name="upload-masterloan-deduction"),
    
    path('masterdeduction/<int:pk>/',MasterDeductionDetail.as_view(), name="update-masterdeduction"),
    
    path('masterdeduction/list/',ListMasterDeduction.as_view(), name="list-masterdeduction"),
    
    path('summary-list/',ListMonthlySummary.as_view(),name="summary-list"),
    
    # loan deductions
    path('deduction-list/',DeductionsList.as_view(),name="deduction-list"),
    
    path('deduction/<int:pk>/',DeductionDetail.as_view(),name="deduction-detail"),
    
    # create bulk deduction from master records
    path('bulk-deduction/',CreateBulkLoanDeduction.as_view(),name="bulk-deduction"),
    
    # create a single loan deduction given a loan id
    path("deduction/<int:loan_pk>/create/", DeductionCreate.as_view(), name="deduction-create"),
    
    # given dates
    path('balances/<str:startdate>/<str:enddate>/',ListBalances.as_view(),name="list-balances"),
    
    # given a loan id
    path('loan-balance/<int:pk>/',IndividualLoanBalance.as_view(),name="loan-balances"),
    
    path('loan-statement/<int:userid>/<str:startdate>/<str:enddate>/',LoanStatement.as_view(), name="loan-statement"),
    
    # Master Savings URL
    path('mastersaving/upload/',MasterSavingUpload.as_view(), name="upload-mastersaving-deduction"),
    
    path('mastersaving/list/',ListMasterSaving.as_view(), name="list-mastersaving"),
    
    path('mastersaving/<int:pk>/',MasterSavingDetail.as_view(), name="mastersaving-detail"),
    
    # create bulk saving deduction from master saving records
    path('bulk-savingdeduction/',CreateBulkSaving.as_view(),name="bulk-savingdeduction"),
    
    path('saving-list/',SavingsList.as_view(),name="saving-list"),
    
    # saving detail given a saving id
    path('<int:pk>/saving/',SavingDetail.as_view(),name="saving-detail"),
    
    # create saving given userid
    path('saving-create/<int:userid>/',CreateSaving.as_view(),name="saving-create"),
    
    # list saving given userid
    path('<int:pk>/user-saving/',ListUserSavings.as_view(),name="user-saving"),
    
    # statement of saving
    path('<int:pk>/<str:startdate>/<str:enddate>/mystatement/',StatementofSavings.as_view(),name="saving-statement"),
    
    # All statement by date range
    path('<str:startdate>/<str:enddate>/allstatement/',allStatementByDate.as_view(),name="statement-by-date"),
    

#   path('loans/',LoanList.as_view(),name='loans'),
#   path('<int:pk>/loans/', LoansByProduct.as_view(), name="product-loans"),
#   path('loan/<int:pk>/', LoanDetail.as_view(),name='loan-detail'),
# #   
    
    # ***************************************************
    
    # path("ebooks/<int:pk>/", EbookDetailAPIView.as_view(), name="ebook-detail"),
    # path("ebooks/<int:ebook_pk>/review/", ReviewCreateAPIView.as_view(), name="ebook-review"),
    # path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),
    # # path("journalists/", JournalistCreateListAPIView.as_view(), name="journalist-list"),
]