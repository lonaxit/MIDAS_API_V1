from email.policy import default
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone


class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    staff_id = models.BigIntegerField(null=True, blank=True)
    home_address = models.CharField(max_length=500, null=True,blank=True)
    dept = models.CharField(max_length=500, null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,blank=True)
    employment_type = models.CharField(max_length=100, null=True,blank=True)
    job_cadre = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    marital_status = models.CharField(max_length=25, null=True,blank=True)
    nok_fullName = models.CharField(max_length=200,null=True,blank=True)
    nok_phone = models.CharField(max_length=25, null=True,blank=True)
    nok_relationship = models.CharField(max_length=50, null=True,blank=True)
    bank = models.CharField(max_length=50, null=True,blank=True)
    bank_account= models.CharField(max_length=20, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,default=timezone.now)
    updated = models.DateTimeField(auto_now=True,default=timezone.now)
 
    
    
    def __str__(self):
        return self.user.username
    
    
class ProductScheme(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,default=timezone.now)
    updated = models.DateTimeField(auto_now=True,default=timezone.now)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True,blank=True)
    product_scheme = models.ForeignKey(ProductScheme,on_delete=models.DO_NOTHING,related_name='products')
    created = models.DateTimeField(auto_now_add=True,default=timezone.now)
    updated = models.DateTimeField(auto_now=True,default=timezone.now)
    
    def __str__(self):
        return self.name

class Loan(models.Model):
    owner = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='loanowner')
    guarantor_one = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='loanguarantorone',null=True, blank=True, default=None)
    guarantor_two = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='loanguarantortwo', null=True, blank=True,default=None)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,related_name='loans')
    loan_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    transaction_code = models.BigIntegerField(null=True, blank=True)
    applied_amount = models.DecimalField(max_digits=20,decimal_places=2)
    approved_amount = models.DecimalField(max_digits=20,decimal_places=2)
    monthly_deduction = models.DecimalField(max_digits=20,decimal_places=2)
    net_pay = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    tenor = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(36)])
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='loancreator')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.product.name
    
    
class MasterLoanDeduction(models.Model):
    
    name= models.CharField(max_length=200)
    ippis_number = models.PositiveBigIntegerField()
    narration = models.CharField(max_length=300, null=True,blank=True)
    entry_date = models.DateField()
    active = models.BooleanField(default=True)
    transaction_code = models.BigIntegerField()
    cumulative_amount = models.DecimalField(max_digits=20,decimal_places=2)
    # balance = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='masterloandeduction')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.name
    

class MasterLoanDeductionSummary(models.Model):

    active = models.BooleanField(default=True)
    transaction_code = models.BigIntegerField()
    transaction_date = models.DateField()
    monthly_cumulative = models.DecimalField(max_digits=20,decimal_places=2)

    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='masterloansummary')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.transaction_code
    


class Deduction(models.Model):

    loanee = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='deductionuser')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE,related_name='deductions')
    credit = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    debit = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    # balance = models.DecimalField(max_digits=20,decimal_places=2)
    narration = models.CharField(max_length=250)
    transaction_code = models.BigIntegerField()
    transaction_date = models.DateField()
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        
         ordering = ['-transaction_date']
        # get_latest_by = "transaction_date"
    
    def __str__(self):
        return self.description
        
    
    
class SavingMaster(models.Model):
    name = models.CharField(max_length=200)
    ippis_number =models.PositiveBigIntegerField()
    narration = models.CharField(max_length=300, null=True,blank=True)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    transaction_code =models.BigIntegerField()
    active =models.BooleanField(default=True)
    transaction_date = models.DateField()
    upload_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='savingmasteruser')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Saving(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='savinguser')
    credit = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    debit = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    transaction_code = models.BigIntegerField()
    transaction_date = models.DateField()
    narration = models.CharField(max_length=350)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='savingcreatedby')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        ordering = ['-transaction_date']
    
    def __str__(self):
        return self.user.last_name
    
class MasterSavingSummary(models.Model):
    
    active = models.BooleanField(default=True)
    transaction_code = models.BigIntegerField()
    transaction_date = models.DateField()
    monthly_cumulative = models.DecimalField(max_digits=20,decimal_places=2)
    
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='mastersavingsummary')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.transaction_code    
    
    

# class Loanledger(models.Model):
#     user =models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="ledgeruser")
#     loan = models.ForeignKey(Loan,on_delete=models.CASCADE,related_name="ledgerloans")
#     description = models.CharField(max_length=250)
#     transaction_date =models.DateField()
#     transaction_code = models.BigIntegerField()
#     credit = models.DecimalField(max_digits=20,decimal_places=2)
    
    

    
    
