from urllib import response
from xml.dom import ValidationErr
from django.shortcuts import render

from rest_framework.views import APIView
# from rest_framework import status,permissions

from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers  import *
# using permissions 
from rest_framework.permissions import *
from core.api.permissions import *
from django.contrib.auth.hashers import make_password

# user creation view 
class RegistrationView(APIView):
    
    permission_classes = [IsAuthenticated,IsAuthOrReadOnly]
    
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
 
#  get logged in user info
    
class RetrieveUserView(APIView):
    
    permission_classes = [IsAuthenticated,IsAuthOrReadOnly]
    
    def get(self,request):
        
        # try:
        user = request.user
        user = UserSerializer(user)
        return Response(
                {'user':user.data},
                status= status.HTTP_200_OK
            )
       
            

class retrieveAllUsers(APIView):
    permission_classes = [IsAuthenticated,IsAuthOrReadOnly]
    
    
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
# update user
class UpdateUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerializer
    permission_classes =[IsAuthenticated & IsAuthOrReadOnly]
    

# Update password for user given a user id
class UpdateUserPassword(APIView):
    
    permission_classes=[IsAuthenticated & IsAuthOrReadOnly]
    # throttle_classes= [AnonRateThrottle]
    
    # def get(self,request,pk):
        
    #     try:
    #         user = User.objects.get(pk=pk)
    #     except User.DoesNotExist:
            
    #         # creating a custom message
    #         return Response({'Error': 'Not Found'},
    #                status=status.HTTP_404_NOT_FOUND
    #                )
             
    #     serializer = UpdateUserPasswordSerializer(user)
    #     return Response(serializer.data)
    
    
    def put(self,request,pk):
        
        
        user = User.objects.get(pk=pk)
        password = make_password(request.data['password'])
        user.password = password
        user.save()
        return Response('Password Reset Successful!')
    
    

# Update password for user given a username
class UpdatePasswordUsername(APIView):
    
    # permission_classes=[IsAuthOnly]
    # throttle_classes= [AnonRateThrottle]
    
    def put(self,request):
        
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
            password = make_password(request.data['password'])
            
            user.password = password
            user.save()
            return Response('Password Reset Successful!')
        
        except User.DoesNotExist:
            raise ValidationErr('Username does not exist')
        
        
      
        
    