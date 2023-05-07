from dataclasses import fields
from rest_framework import serializers
# import models
from core.models import *
from django.db.models import Q, Sum, Avg, Max, Min, Count
from django.db.models import F

User = get_user_model()


class DeductionSerializer(serializers.ModelSerializer):
    # loan_balance = serializers.SerializerMethodField()
    loan = serializers.CharField(source='loan.product.name') 
    loanee = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    loan = serializers.StringRelatedField()
    loan_id = serializers.SerializerMethodField()
    class Meta:
        model = Deduction
        fields = "__all__"
        ordering=['transaction_date']
        
    def get_loan_id(self,object):
        return object.loan.pk
        
    # def get_loan_balance(self,object):
        # previous_balances = Deduction.objects.filter(transaction_date__lt=obj.transaction_date)
        # total_debits = previous_balances.aggregate(total_debits=Sum('debit'))['total_debits'] or 0
        # total_credits = previous_balances.aggregate(total_credits=Sum('credit'))['total_credits'] or 0
        #trnxDiff = total_credits - total_debits
        # return loan.approved_amount-trnxDiff
        
        
       
    #     allDeductions = Deduction.objects.filter(Q(transaction_date=object.transaction_date) & Q(loan=object.loan.pk))
        
    #     if (allDeductions.count() > 1):
    #         # select records greater than this date
    #         GreaterDeductions = Deduction.objects.filter(Q(transaction_date__lt=object.transaction_date) & Q(loan=object.loan.pk))
            
    #         totalcredit = GreaterDeductions.aggregate(credit=Sum('credit'))
                            
    #         totaldebit = GreaterDeductions.aggregate(debit=Sum('debit'))
    #         Greatercredit = totalcredit['credit']
    #         Greaterdebit = totaldebit['debit']
        
    #         if not Greatercredit:
    #             Greatercredit=0
    #         if not Greaterdebit:
    #             Greaterdebit=0 
            
    #         Deductions = Deduction.objects.filter(Q(transaction_date=object.transaction_date) & Q(loan=object.loan.pk) & Q(pk__lte=object.pk))
    
    #         totalcredit = Deductions.aggregate(credit=Sum('credit'))
                            
    #         totaldebit = Deductions.aggregate(debit=Sum('debit'))
    #         credit = totalcredit['credit']
    #         debit = totaldebit['debit']
        
    #         if not credit:
    #             credit=0
    #         if not debit:
    #             debit=0            
                            
    #         payments = credit + Greatercredit - debit+Greaterdebit
        
    #         return object.loan.approved_amount-payments
            
        
    #     all_Deductions = Deduction.objects.filter(Q(transaction_date__gte= object.transaction_date) & Q(loan=object.loan.pk))
        
    #     totalcredit = all_Deductions.aggregate(credit=Sum('credit'))
                            
    #     totaldebit = all_Deductions.aggregate(debit=Sum('debit'))
    #     credit = totalcredit['credit']
    #     debit = totaldebit['debit']
        
    #     if not credit:
    #         credit=0
    #     if not debit:
    #         debit=0            
                            
    #     payments = credit - debit
        
    #     return object.loan.approved_amount-payments
        
        
    
# Serializer to create and List Loans providing user id on the form
class LoanListCreateSerializer(serializers.ModelSerializer):
    
    created_by = serializers.StringRelatedField()
    total_balance = serializers.SerializerMethodField()
    totaldeduction = serializers.SerializerMethodField()
    loan_owner = serializers.SerializerMethodField()
    loan_owner_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Loan
        fields = "__all__"
    
    def get_total_balance(self,object):
            
        allDeductions = Deduction.objects.filter(loan=object.pk)
        
        totalcredit = allDeductions.aggregate(credit=Sum('credit'))
                        
        totaldebit = allDeductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        return object.approved_amount - payments
    
    
    def get_totaldeduction(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk)
        
        totalcredit = allDeductions.aggregate(credit=Sum('credit'))
                        
        totaldebit = allDeductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        return  credit - debit
        
        # return object.approved_amount - payments
    
    def get_loan_owner(self,object):
        
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.last_name + ' ' + Owner.first_name
    
    def get_loan_owner_id(self,object):
            
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.pk
    
    def get_product_name(self,object):
            
        product = Product.objects.get(pk=object.product.pk)
        return product.name

   
class LoanSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    
    total_balance = serializers.SerializerMethodField()
    totaldeduction = serializers.SerializerMethodField()
    loan_owner = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    loan_owner_id = serializers.SerializerMethodField()
    totalCredit =serializers.SerializerMethodField()
    totalDebit =serializers.SerializerMethodField()
  
    # deductions = DeductionSerializer(many=True,read_only=True)
    
    class Meta:
        model = Loan
        fields = "__all__"

    def get_total_balance(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk)
        
        totalcredit = allDeductions.aggregate(credit=Sum('credit'))
                        
        totaldebit = allDeductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        return object.approved_amount - payments
    
    
    def get_totaldeduction(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk)
        
        totalcredit = allDeductions.aggregate(credit=Sum('credit'))
                        
        totaldebit = allDeductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        return  credit - debit
        
        # return object.approved_amount - payments
    
    def get_loan_owner(self,object):
        
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.last_name + ' ' + Owner.first_name
    
    def get_loan_owner_id(self,object):
            
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.pk
    
    def get_product_name(self,object):
            
        product = Product.objects.get(pk=object.product.pk)
        return product.name
    
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


# Loan Detail Serializer
class LoanDetailSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    
    total_balance = serializers.SerializerMethodField()
    totaldeduction = serializers.SerializerMethodField()
    loan_owner = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    loan_owner_id = serializers.SerializerMethodField()
    totalCredit =serializers.SerializerMethodField()
    totalDebit =serializers.SerializerMethodField()
    deductions = DeductionSerializer(many=True,read_only=True)
    
    class Meta:
        model = Loan
        fields = "__all__"

    def get_total_balance(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk)
        
        totalcredit = allDeductions.aggregate(credit=Sum('credit'))
                        
        totaldebit = allDeductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        return object.approved_amount - payments
    
    
    def get_totaldeduction(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk)
        
        totalcredit = allDeductions.aggregate(credit=Sum('credit'))
                        
        totaldebit = allDeductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        return  credit - debit
        
        # return object.approved_amount - payments
    
    def get_loan_owner(self,object):
        
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.last_name + ' ' + Owner.first_name
    
    def get_loan_owner_id(self,object):
            
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.pk
    
    def get_product_name(self,object):
            
        product = Product.objects.get(pk=object.product.pk)
        return product.name
    
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
    
# class ProductSerializer(serializers.ModelSerializer):
#     loans = LoanSerializer(many=True, read_only=True)
#     product_scheme = serializers.StringRelatedField(read_only=True)
    
    
#     class Meta:
#         model=Product
#         fields= '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    loans = LoanSerializer(many=True, read_only=True)
    # product_scheme = serializers.StringRelatedField(read_only=True)
    scheme = serializers.SerializerMethodField()

   
    
    class Meta:
        model=Product
        fields= '__all__'
    
    def get_scheme(self,object):
        
        Scheme = ProductScheme.objects.get(pk=object.product_scheme.pk)
        return Scheme.name
        
        
class ProductSchemeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model=ProductScheme
        # exclude = ('id',)
        fields= '__all__'
        
        
class LoanUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    

class MonthlyLoanDeductionSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = MasterLoanDeduction
        fields = "__all__"

    def get_total_amount(self, obj):
        previous_amount = MasterLoanDeduction.objects.filter(created__lte=obj.created)
        total = sum(item.cumulative_amount for item in previous_amount)
        return total + obj.cumulative_amount
    

class MasterLoanDeductionUploadSerializer(serializers.Serializer):
 
        file = serializers.FileField()
        

class MasterLoanDeductionSummarySerializer(serializers.ModelSerializer):
    narration = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = MasterLoanDeductionSummary
        fields = "__all__"
        
    
    def get_narration(self,object):
        
        LoanObj = MasterLoanDeduction.objects.filter(transaction_code=object.transaction_code).first()
        return LoanObj.narration
    
    def get_date(self,object):
        
        LoanQueryObj = MasterLoanDeduction.objects.filter(transaction_code=object.transaction_code).first()
        return LoanQueryObj.entry_date

# deduction serializer
    

# get cumulative loan balances of all active loans
class AllLoanBalancesByDateSerializer(serializers.ModelSerializer):
    
    balance = serializers.SerializerMethodField()
    loan_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        # fields ="__all__"
        fields  = ('id', 'owner','balance','loan_owner')
        
    def get_loan_owner(self,object):
            
        Owner = User.objects.get(pk=object.owner.pk)
        return Owner.last_name + ' ' + Owner.first_name
       
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
    
# Get individual Loan Balance

class IndividualLoanBalanceSerializer(serializers.ModelSerializer):
    
    deductions = serializers.SerializerMethodField()
    principal =serializers.SerializerMethodField()
    totalCredit =serializers.SerializerMethodField()
    totalDebit =serializers.SerializerMethodField()
    balance =serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Loan
      
        fields  = ('id', 'product','owner','deductions','principal','totalCredit','totalDebit','balance','approved_amount','monthly_deduction','start_date','end_date','product_name')
        
    def get_deductions(self,object):
        
        allDeductions = Deduction.objects.filter(loan=object.pk).values()
        
        return allDeductions
    def get_product_name(self,object):
            
        product = Product.objects.get(pk=object.product.pk)
        return product.name
    
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
        

# User Loan Statement By Date
class UserLoanStatementByDateSerializer(serializers.ModelSerializer):
    
    deductions = serializers.SerializerMethodField()
    principal =serializers.SerializerMethodField()
    totalCredit =serializers.SerializerMethodField()
    totalDebit =serializers.SerializerMethodField()
    balance =serializers.SerializerMethodField()
    
    product = serializers.CharField(source='product.name') 
    
    class Meta:
        model = Loan
      
        fields  = ('id', 'product','owner','deductions','principal','totalCredit','totalDebit','balance')
        
    def get_deductions(self,object):
        start_date = self.context['startdate']
        end_date = self.context['enddate']
        
        allDeductions = Deduction.objects.filter(loan=object.pk,transaction_date__gte=start_date,transaction_date__lte=end_date)
    
        return list(allDeductions.values())
    
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


# upload saving master record serializer
class SavingMasterUploadSerializer(serializers.Serializer):
     
        file = serializers.FileField()

class SavingMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SavingMaster
        fields = "__all__"

class SavingSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    user_id = serializers.SerializerMethodField()
    totalCredit = serializers.SerializerMethodField()
    balance =serializers.SerializerMethodField()

    class Meta:
        model = Saving
        fields = "__all__" 
         
    def get_balance(self,object):
        
        
        allDeductions = Saving.objects.filter(Q(transaction_date = object.transaction_date) & Q(user=object.user.pk))
        
        if (allDeductions.count() > 1):
            # select records greater than this date
            GreaterDeductions = Saving.objects.filter(Q(transaction_date__gt=object.transaction_date) & Q(user=object.user.pk))
            
            totalcredit = GreaterDeductions.aggregate(credit=Sum('credit'))
                            
            totaldebit = GreaterDeductions.aggregate(debit=Sum('debit'))
            Greatercredit = totalcredit['credit']
            Greaterdebit = totaldebit['debit']
        
            if not Greatercredit:
                Greatercredit=0
            if not Greaterdebit:
                Greaterdebit=0 
            
            Deductions = Saving.objects.filter(Q(transaction_date=object.transaction_date) & Q(user=object.user.pk) & Q(pk__lte=object.pk))
    
        
            totalcredit = Deductions.aggregate(credit=Sum('credit'))
                            
            totaldebit = Deductions.aggregate(debit=Sum('debit'))
            credit = totalcredit['credit']
            debit = totaldebit['debit']
        
            if not credit:
                credit=0
            if not debit:
                debit=0            
                            
            payments = credit + Greatercredit - debit+Greaterdebit
        
            return payments
            
        
        all_Deductions = Saving.objects.filter(Q(transaction_date__gte= object.transaction_date) & Q(user=object.user.pk))
        
        totalcredit = all_Deductions.aggregate(credit=Sum('credit'))
                            
        totaldebit = all_Deductions.aggregate(debit=Sum('debit'))
        credit = totalcredit['credit']
        debit = totaldebit['debit']
        
        if not credit:
            credit=0
        if not debit:
            debit=0            
                            
        payments = credit - debit
        
        return payments
      
    def get_user_id(self,object):
        Owner = User.objects.get(pk=object.user.pk)
        return Owner.id
    
    def get_totalCredit(self,object):
        
        totalCredit = Saving.objects.filter(user=object.user.pk).aggregate(credit=Sum('credit'))
        
        totalDebit = Saving.objects.filter(user=object.user.pk).aggregate(debit=Sum('debit'))
        
    
        credit = totalCredit['credit']
        debit = totalDebit['debit']
       
        if not credit:
            credit=0
        if not debit:
            debit=0            
                        
        payments = credit - debit
        
        return payments
    
# ******************************* 
# class FileUploadSerializer(serializers.Serializer):
#     file = serializers.FileField()
    
    
# class SaveFileSerializer(serializers.Serializer):
    
#     class Meta:
#         model = File
#         fields = "__all__"



# SerializerMethod
# ***************************************************************
# Using serializer method field


# Returns the number of ratings
    # def get_count_feedbacks(self, instance):
    #     return instance.business_account.feedbackmodel_set.count()  

    # Returns the average rating
    # def get_average_rating(self, instance)
    #     return instance.business_account.feedbackmodel_set.aggregate(average_rating=('rating'))['average_rating']
    
# **************************************************************



# *****************************************************
# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     ...
# class Offer(models.Model):
#     item = models.ForeignKey(Item)
#     ...
# class Purchase(models.Model):
#     offer = models.ForeignKey(Offer)

# def get_purchase_count(item):
#         return Purchase.objects.filter(
#             offer__item=item, 
#             state="success").count()
# ****************************************************************

# ******* show age to admin only hidden for other users
# def calculate_age(self, instance):
#     request = self.context.get('request')
#     user = request.user
#     if user.is_authenticated() and user.is_admin:
#         return datetime.datetime.now().year - instance.dob.year
#     return 'Hidden'


# using re_presentation to show fields conditionally in a serializers
# class UserSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name')

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if instance.is_superuser:
#             representation['admin'] = True
#         return representation


# grouping result in aquery
# tickets = (MovieTicket.objects
#             .filter(user=request.user)
#             .values('show')
#             .annotate(last_booking=Max('booked_at'))
#             .order_by('-last_booking')
# )