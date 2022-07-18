from dataclasses import fields
from rest_framework import serializers

# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model
User = get_user_model()

# user app
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','other_name','is_employee','is_account','is_normal')
        


