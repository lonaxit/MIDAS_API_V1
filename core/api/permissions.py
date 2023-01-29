from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self,request,view,obj):
        # option 1 code
        # admin_permission = bool(request.user and request.user.is_staff)
        
        # # try to find out if its get request or the user has permission
        # return request.method == 'GET' or  admin_permission
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
    
    
# another custom permission
class IsReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
        
        # check for read only 'GET' method 
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # review_user is a property of the Review Model
            return obj.review_user == request.user or request.user.is_staff
        
        
class IsLoanOwnerOrStaff(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
        # option 1 code
        # admin_permission = bool(request.user and request.user.is_staff)
        
        # # try to find out if its get request or the user has permission
        # return request.method == 'GET' or  admin_permission
        loan_owner_permission =  obj.owner == request.user or request.user.is_employee or request.user.is_account
       
        return bool(loan_owner_permission)


class IsLoanOwnerOnly(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
  
        loan_owner_permission =  obj.owner == request.user
       
        return bool(loan_owner_permission)


class IsAuthOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        if(request.user.is_employee or request.user.is_account or request.user.is_staff):
            return True
     
    
    def has_object_permission(self,request,view,obj):
             
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user.is_employee or request.user.is_account)
    
