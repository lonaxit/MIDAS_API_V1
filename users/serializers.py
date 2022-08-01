from dataclasses import fields
import profile
from rest_framework import serializers
from core.models  import Profile

# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model
User = get_user_model()

# user app
class UserSerializer(serializers.ModelSerializer):
    
    # profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','other_name','is_employee','is_account','is_normal')
        
# 
class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','password')


class UpdatePasswordWithUsernameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','password','username')
        


