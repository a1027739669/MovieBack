from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json
from program import itemrec
import multiprocessing
file_path="data/rating.csv"
itemBasedCF = itemrec.ItemBasedCF()
itemBasedCF.load_data(file_path)
itemBasedCF.data_transfer()
itemBasedCF.similarity()
from .models import *
# Create your views here.

def iter_recommend(request):
    userid=request.get('userid')
    print(userid)
    # result=itemBasedCF.recommendation(userid)
    return JsonResponse("hello")