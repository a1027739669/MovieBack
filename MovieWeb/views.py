from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import simplejson
import time
from program.itemrec import *
from program.cbrec import *
from program import spi
import multiprocessing
from .models import *
# Create your views here.
import threading
import re
import uuid
import requests
import os
import numpy
import imghdr
import time
from PIL import Image
from MovieWeb.models import*
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

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
    download()
    return HttpResponse("hello")

def user_login(request):
    req=simplejson.loads(request.body)
    user=User.objects.filter(username=req['username'],password=req['password'])
    data={}
    if(not user.exists()):
        data['success']=False
        data['error']='用户名或密码错误!'
    else:
        data['success']=True
        data['data']=model_to_dict(user[0])
    return HttpResponse(simplejson.dumps(data))

def cou_ui():
    userpres=[x for x in UserPreference.objects.all()]
    user_pre={}
    itemids={}
    users=User.objects.all()
    all_items = list(Movie.objects.values_list('movieid', flat=True))
    none_items={}
    movie_dict={}
    movies=Movie.objects.all()
    movid_ferture={}
    for movie in movies:
        movid_ferture[movie.movieid]=[eval(x.split(':')[1]) for x in movie.feature.split('/')[:-1]]
    for movie in movies:
        movie_dict[movie.movieid]=movie
    for user in users:
        user_pre[user.userid]=[eval(x.split(':')[1]) for x in user.preference.split('/')[:-1]]
        itemids[user.userid]=[eval(x) for x in user.watchitems.split('/')[0:-1]]
    for user in users:
        none_items[user.userid] = list(set(all_items) - set(itemids[user.userid]))

    print('start')
    for userpre in userpres:
        if(userpre.userid%1000==0):
            print(userpre.userid)
        result = {}
        for movie_id in none_items[userpre.userid]:
            Uia = sum(np.array(user_pre[userpre.userid]) * np.array(movid_ferture[movie_id]))  # 用杰卡德相似系数
            result.setdefault(movie_id, Uia)
            # result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))  # 计算电影偏好排序结果
        ans = ''  # 用户偏好度 用字符串表示
        for key, value in result.items():
            ans.join([str(key),':',str(value),'/'])
        userpre.userpre=ans
        userpre.save()

def download():
    movies=Movie.objects.all()
    for movie in movies:
        spi.download_image(movie.movieid)




