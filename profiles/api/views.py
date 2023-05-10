import random
import string

from profiles.api.serializers import *
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

from core.api.permissions import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



User = get_user_model()

class ProfileRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes=[IsAuthenticated]
    

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class =ProfileSerializer
    permission_classes = [IsAuthenticated]
    
class GetProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class =  ProfileListSerializer
    permission_classes = [IsAuthenticated]  


# Get a user's profile detail 
class GetProfile(generics.RetrieveAPIView):
  
    # serializer_class = ProfileSerializer
    serializer_class = ProfileListSerializer
    permission_classes= [IsAuthenticated & IsAuthOrReadOnly]
    lookup_field ='user'
    
    def get_queryset(self):
    
        return Profile.objects.all()

# 
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileListSerializer
    permission_classes= [IsAuthenticated & IsAuthOrReadOnly]

    def get_object(self):
        # return self.request.user.profile
        user = self.request.user
        
        return Profile.objects.filter(user=user)



# search user using the search bar
class ProfileSearch(generics.RetrieveAPIView):
    """
    List Method

    Parameters:
        user id

    Returns:
        A user profile
    """
      
    serializer_class = ProfileSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    lookup_field ='user'
    
    # works as well
    # class LoansByUser(APIView):
          
    # serializer_class = LoanSerializer
    # permission_classes =[IsAuthenticated]
    # lookup_field ='owner'
    # def get(self,request,*args,**kwargs):
        
    #     user_pk = self.kwargs['pk']
    #     try:
    #         user = User.objects.get(pk=user_pk)
    #         Loans = Loan.objects.filter(owner=user)
            
    #         if not Loans:
    #             raise ValidationError('User Has No Loans!')
    #         return Response(list(Loans.values()))
        
    #     except User.DoesNotExist:
            
    #         return Response({'Error': 'User Not Found!'},
    #                 status=status.HTTP_404_NOT_FOUND)
            
            
    # # over writing default queryset 
    # def get_queryset(self):
    #     # get the wachlist pk
    #     user_pk = self.kwargs['pk']
    #     try:
    #         profile = Profile.objects.filter(user=user_pk)
    #         if not profile:
    #             raise ValidationError('User Does Not Exist')
    #         return profile
        
    #     except Profile.DoesNotExist:
            
    #         # get_queryset shoud not return a response
    #         # return Response({'Error': 'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
    #         raise ValidationError('User Does Not exist')
        


# class ProfileUpdate(generics.UpdateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer