from dataclasses import fields
from rest_framework import serializers
# import models
from core.models import *
from django.db.models import Q, Sum, Avg, Max, Min, Count


# get cumulative balances of all loans for a user
class UserCumulativeBalancesSerializer(serializers.ModelSerializer):
    
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        # fields ="__all__"
        fields  = ('id', 'owner','balance')
        
        
    def get_balance(self,object):
        
        start_date = self.context['startdate']
        end_date = self.context['enddate']
        
        principal = Loan.objects.filter(owner=object.owner).aggregate(pay=Sum('approved_amount'))
        
        totalCredit = Deduction.objects.filter(loanee=object.owner,transaction_date__gte=start_date,transaction_date__lte=end_date).aggregate(credit=Sum('credit'))
        
        totalDebit = Deduction.objects.filter(loanee=object.owner,transaction_date__gte=start_date,transaction_date__lte=end_date).aggregate(debit=Sum('debit'))
        
        #  result = list(Subject.objects.filter(subjectteacher__classroom_id=pk,subjectteacher__teacher_id=loggedin).values())

        credit = totalCredit['credit']
        debit = totalDebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        bal = principal['pay']-payments
        
        return bal
    
    
    
    
# Get individual Loan History
class loanHistorySerializer(serializers.ModelSerializer):
    
    deductions = serializers.SerializerMethodField()
    principal =serializers.SerializerMethodField()
    totalCredit =serializers.SerializerMethodField()
    totalDebit =serializers.SerializerMethodField()
    balance =serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
      
        fields  = ('id', 'product','owner','deductions','principal','totalCredit','totalDebit','balance')
        
    def get_deductions(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk).values()
        
        return allDeductions
    
    def get_principal(self,object):
        
        return object.approved_amount
    
    def get_totalCredit(self,obj):
        
        credit = Deduction.objects.filter(loan=obj.pk).aggregate(credit=Sum('credit'))
        credit = credit['credit']
        if not credit:
            credit=0
            
        return credit
    
    def get_totalDebit(self,obj):
            
        debit = Deduction.objects.filter(loan=obj.pk).aggregate(debit=Sum('debit'))
        
        debit = debit['debit']
        if not debit:
            debit=0
            
        return debit
         
    def get_balance(self,object):
        
        totalCredit = Deduction.objects.filter(loan=object.pk).aggregate(credit=Sum('credit'))
        
        totalDebit = Deduction.objects.filter(loan=object.pk).aggregate(debit=Sum('debit'))
        
    
        credit = totalCredit['credit']
        debit = totalDebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        bal = object.approved_amount-payments
        
        return bal
        