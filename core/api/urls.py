from django.urls import path,include

from core.api.views import *

urlpatterns =[
    
    path("schemes/", ProductSchemeListCreate.as_view(), name="schemes"),
    
    path("scheme-detail/<int:pk>/", ProductSchemeDetail.as_view(), name="scheme-detail"),
    
    path("product-list/", ProductList.as_view(), name="product-list"),
    path("product-create/<int:pk>/", ProductCreate.as_view(), name="product-create"),
    path("product-detail/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    
    path('loan-upload/', LoanUpload.as_view(),name='loan-upload'),
    path('loan-list-create/', LoanListCreate.as_view(), name='loan-list-create'),
    path('loan/<int:pk>/', LoanDetail.as_view(), name='loan-detail'),
    path('product/<int:pk>/loans/', LoansByProduct.as_view(), name="product-loans"),
    
    
    path('masterdeduction/upload',MonthlyLoanDeductionUpload.as_view(), name="upload-masterloan-deduction"),
    path('masterdeduction/create',MonthlyLoanDeductionUpload.as_view(), name="upload-masterloan-deduction"),
    
    path('summary-list/',ListMonthlySummary.as_view(),name="summary-list"),
    
    path('deduction-list/',DeductionsList.as_view(),name="deduction-list"),
    path('create-deduction/<int:pk>/',DeductionsList.as_view(),name="create-deduction"),
    
    

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