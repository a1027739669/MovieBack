from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import simplejson
import time
from program.itemrec import *
from program.cbrec import *
import multiprocessing
from .models import *
# Create your views here.

file_path="data/rating.csv"
# itemBasedCF = itemrec.ItemBasedCF()
# itemBasedCF.load_data(file_path)
# itemBasedCF.data_transfer()
# itemBasedCF.similarity()

def iter_recommend(request):
    userid=request.GET['userid']
    result={}
    # result=itemBasedCF.recommendation(userid)
    return HttpResponse(result)

def set_watch(request):
    # i=1
    # ratings=Rating.objects.all()
    # for rating in ratings:
    #     user=User.objects.get(userid=rating.userid)
    #     user.watchitems+=str(rating.movieid)+'/'
    #     user.save()
    #     if(i%10000==0):
    #         print(i)

    # User.objects.all().update(watchitems='')

    # users=User.objects.all()
    # i=1
    # for user in users:
    #     start=time.time()
    #     rs=[]
    #     ratings=Rating.objects.filter(userid=user.userid)
    #     for rating in ratings:
    #         if(rating.movieid not in rs):
    #             rs.append(rating.movieid)
    #         else:
    #             rating.delete()
    #
    #     print(i)
    #     end=time.time()
    #     print(end-start)
    #     i+=1
    cbrec=CBRec()
    item=ItemBasedCF()
    print(cbrec.recommend(1))
    print(item.recommend(1))
    return HttpResponse("hello")
