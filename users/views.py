from urllib import response
from django.shortcuts import render

from rest_framework.views import APIView
# from rest_framework import status,permissions

from rest_framework import status
# from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers  import *
# using permissions 
from rest_framework.permissions import *


# user creation view 
class RegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        try:
            data = request.data
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            password = data['password']
            re_password = data['re_password']
            # is_employee = data['is_employee']
            
            # if is_employee=='True':
            #     is_employee=True
            # else:
            #     is_employee=False
            if not password:
                 return Response(
                        {'msg':'Fill the records'},
                        status = status.HTTP_400_BAD_REQUEST
                        )
            
            if password == re_password:
                if len(password) >=8:
                    
                    if not User.objects.filter(username=username).exists():
                        
                         User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password)
                            
                         return Response(
                            {'msg':'User created successfuly'},
                            status = status.HTTP_201_CREATED
                            )
                        
                        # if not is_employee:
                        #     User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password)
                            
                        #     return Response(
                        #     {'success':'User created successfuly'},
                        #     status = status.HTTP_201_CREATED
                        #     )
                        # else:
                        #     User.objects.create_employee(first_name=first_name,last_name=last_name,username=username,password=password)
                            
                        #     return Response(
                        #     {'success':'Employee created successfuly'},
                        #     status = status.HTTP_201_CREATED
                        #     )
                            
                    else:
                        
                        return Response(
                        {'msg':'User already exist'},
                        status = status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                    {'msg':'Password must be at least 8 characters'},
                    status = status.HTTP_400_BAD_REQUEST
                    )
            
            else:
                return Response(
                {'msg':'Password mismatch'},
                status = status.HTTP_400_BAD_REQUEST
                )
                 
            
        except:
            return Response(
                {'msg':'Something went wrong when creating an account!'},
                status =status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
#  get user info
class RetrieveUserView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        
        # try:
        user = request.user
        user = UserSerializer(user)
        return Response(
                {'user':user.data},
                status= status.HTTP_200_OK
            )
        # except:
        #     return Response(
        #         {'error':'Unable to retrieve data'},
        #         status =status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
            

class retrieveAllUsers(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self,request):
        try:
            user = User.objects.all()
            user = UserSerializer(user,many=True)
            return Response(
                {'user':user.data},
                status= status.HTTP_200_OK
            )
        except:
            return Response(
                {'error':'Unable to retrieve data'},
                status =status.HTTP_500_INTERNAL_SERVER_ERROR
            )
