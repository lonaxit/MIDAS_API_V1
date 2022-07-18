from dataclasses import fields
from rest_framework import serializers
# import models
from core.models import *
from django.db.models import Q, Sum, Avg, Max, Min

class LoanSerializer(serializers.ModelSerializer):
    
    totaldebt = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        fields = "__all__"

    def get_totaldebt(self,object):
        # todo
        # you can find aggregate using the product id or loan id from the deductions table
        
        loans = Loan.objects.filter(owner=object.owner).aggregate(debt_sum=Sum('approved_amount'))
        return loans['debt_sum']
    
    
class ProductSerializer(serializers.ModelSerializer):
    loans = LoanSerializer(many=True, read_only=True)
    product_scheme = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=Product
        fields= '__all__'
        
        
class ProductSchemeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model=ProductScheme
        # exclude = ('id',)
        fields= '__all__'
        
        
class LoanUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    



        
# not used
# class MonthlyLoanDeductionSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = MonthlyLoanDeduction
#         fields = "__all__"


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


class DeductionSerializer(serializers.ModelSerializer):
    # deductions = LoanSerializer(many=True, read_only=True)
    class Meta:
        model = Deduction
        fields = "__all__"
    







# scores = scoresList.filter(student=student.student).aggregate(subject_total=Sum('subjecttotal'))
 # scores = Scores.objects.filter(student=studentid,studentclass=classroom,term=termObj,session=sessionObj).aggregate(term_sum=Sum('subjecttotal'))

    # term_sum = scores['term_sum']
    
    
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