from dataclasses import fields
import profile
from rest_framework import serializers
from core.models  import Profile

# IMPORT CUSTOM USER
from django.contrib.auth import get_user_model
from core.api.serializers import *
User = get_user_model()

# user app
class UserSerializer(serializers.ModelSerializer):
    
    savinguser = SavingSerializer(many=True,read_only=True)
    # loanowner = LoanSerializer(many=True,read_only=True)
    
    totalSaving = serializers.SerializerMethodField()
    # balance = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # fields = '__all__'
        # fields = ('id','username','first_name','last_name','other_name','is_employee','is_account','is_normal','is_active','date_joined','savinguser','totalSaving')
        exclude=('groups','user_permissions','date_joined','last_login','password')
        
    
    
    def get_totalSaving(self,object):
            
        totalCredit = Saving.objects.filter(user=object.pk).aggregate(credit=Sum('credit'))
        
        totalDebit = Saving.objects.filter(user=object.pk).aggregate(debit=Sum('debit'))
        
    
        credit = totalCredit['credit']
        debit = totalDebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        return payments
    

class UserOpeningBalanceSerializer(serializers.ModelSerializer):
    
    openingBalance = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','other_name','is_employee','openingBalance')
        
    def get_openingBalance(self,object):
        start_date = self.context['startdate']
        
        allSavings = Saving.objects.filter(user=object.pk,transaction_date__lt=start_date)
    
        totalCredit = allSavings.aggregate(credit=Sum('credit'))
        
        totalDebit = allSavings.aggregate(debit=Sum('debit'))
        
    
        credit = totalCredit['credit']
        debit = totalDebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        
        return payments
        
# 
class UpdateUserPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','password')


class UpdatePasswordWithUsernameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','password','username')
        


