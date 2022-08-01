from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model
User = get_user_model()


class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    ippis = models.BigIntegerField(null=True, blank=True)
    home_address = models.CharField(max_length=350, null=True,blank=True)
    # dob = models.DateField()
    # employment_status = models.CharField(maxlength=100)
    
    avatar = models.ImageField(null=True,blank=True)
    
    
    def __str__(self):
        return self.user.username
    
    
class ProductScheme(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True,blank=True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True,blank=True)
    product_scheme = models.ForeignKey(ProductScheme,on_delete=models.DO_NOTHING,related_name='products')
    
    def __str__(self):
        return self.name

class Loan(models.Model):
    owner = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='loanowner')
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,related_name='loans')
    loan_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    transaction_code = models.BigIntegerField()
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
    credit = models.DecimalField(max_digits=20,decimal_places=2,default="0.00")
    debit = models.DecimalField(max_digits=20,decimal_places=2,default="0.00")
    transaction_code = models.BigIntegerField()
    transaction_date = models.DateField()
    narration = models.CharField(max_length=350)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='savingcreatedby')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
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
    
    

    
    
# 
# class File(models.Model):
#     id = models.CharField(primary_key=True, max_length=6)
#     staff_name = models.CharField(max_length=100)
#     position = models.CharField(max_length=200)
#     age = models.IntegerField()
#     year_joined = models.CharField(max_length=4)
#     def __str__(self):
#         return self.staff_name