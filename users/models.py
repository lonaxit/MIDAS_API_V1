from django.db import models

from django.utils import timezone


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def create_user(self, first_name,last_name,username,ippis_number,dob,dofa,password=None):
        
        if not username:
            raise ValueError('User must have a username and must be unique')
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        if not ippis_number:
            raise ValueError('Please enter an IPPIS NUMBER')
        if ippis_number and isinstance(ippis_number,str):
            raise ValueError('Ippis Number can not be a string')
        if not dob:
            raise ValueError('User must have a date of birth')
        if not dofa:
            raise ValueError('User must have a date of first appointment')
             
        

        user = self.model(
            username=username,
            first_name=first_name,
            last_name = last_name,
            ippis_number = ippis_number,
            dob = dob,
            dofa=dofa
        )

        user.set_password(password)
        
        # when using multple databases
        # user.save(using=self._db)
        user.save()
        return user

    # method to create other roles
    def create_employee(self, first_name,last_name,username, ippis_number,dob,dofa,password=None):
        user = self.create_user(first_name,last_name,username,ippis_number,dob,dofa,password)
        user.is_employee=True
        user.save()
        
        return user
    
    def create_account(self, first_name,last_name,username,ippis_number,dob,dofa,password=None):
        user = self.create_user(first_name,last_name,username,ippis_number,dob,dofa,password)
        user.is_account=True
        user.save()
        
        return user
    
    def create_normal(self, first_name,last_name,username,ippis_number,dob,dofa,password=None):
        user = self.create_user(first_name,last_name,username,ippis_number,dob,dofa,password)
        user.is_normal=True
        user.save()
        
        return user
    
    def create_superuser(self, first_name,last_name,username,ippis_number,dob,dofa,password=None):
        user = self.create_user(first_name,last_name,username,ippis_number,dob,dofa,password)
      
        user.is_superuser = True
        user.is_staff =True
        user.save()
        return user
    
      

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255,blank=True)
    ippis_number = models.BigIntegerField(default=0000000)
    dob = models.DateField(default="2000-01-02")
    dofa = models.DateField(default="2000-01-02")
    # employment_type = models.CharField(max_length=100, null=True,blank=True)
    
    # home_address = models.CharField(max_length=500, null=True,blank=True)
    # gender = models.CharField(max_length=20, null=True,blank=True)
    # job_cadre = models.CharField(max_length=100,null=True,blank=True)
    # phone = models.CharField(max_length=20,null=True,blank=True)
    # email = models.EmailField(null=True, blank=True)
    # marital_status = models.CharField(max_length=25, null=True,blank=True)
    # nok_fullName = models.CharField(max_length=200,null=True,blank=True)
    # nok_phone = models.CharField(max_length=25, null=True,blank=True)
    # nok_relationship = models.CharField(max_length=50, null=True,blank=True)
    # bank = models.CharField(max_length=50, null=True,blank=True)
    # bank_account= models.CharField(max_length=20, null=True,blank=True)
    avatar = models.ImageField(null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_normal = models.BooleanField(default=False)
    is_account =  models.BooleanField(default=False)
    
    
    objects = CustomUserManager()
    
    USERNAME_FIELD ='username'
    REQUIRED_FIELDS = ['first_name','last_name','ippis_number','dob','dofa']
    
    def __str__(self):
        return self.username




