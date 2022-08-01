import random
import string

from profiles.api.serializers import *
# # import models
from core.models import *
from django.contrib.auth import get_user_model
# from django.db.models import Q, Sum, Avg, Max, Min
from django.db import transaction
from django.shortcuts import get_object_or_404
# # from rest_framework import mixins
from rest_framework import generics, status
# # import validation errors
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import *
# # import Response
from rest_framework.response import Response
# # import here below used for class based views
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser,FormParser

import openpyxl



User = get_user_model()

class ProfileRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes=[IsAuthenticated]
    

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class =ProfileSerializer
    permission_classes = [IsAuthenticated]

# class ProfileUpdate(generics.UpdateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer