from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
