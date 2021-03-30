from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.core.cache import cache
import time
from program.itemrec import *
from program.cbrec import *
from program import spi
import random
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
    User.objects.all().update(password='123456789')
    return HttpResponse("hello")

def user_login(request):
    req=json.loads(request.body)
    user=User.objects.filter(username=req['username'],password=req['password'])
    data={}
    if(not user.exists()):
        data['success']=False
        data['error']='用户名或密码错误!'
    else:
        data['success']=True
        data['data']=model_to_dict(user[0])
    return HttpResponse(json.dumps(data))

#获取高评分电影
def get_high_score_movies(request):
    movies=list(Movie.objects.order_by('-score').values()[:10])
    data={}
    data['data']=movies
    data['msg']='高评分电影'
    return HttpResponse(json.dumps(data))

#未登录进行随机推荐
def get_recom_movies_unlogin(request):
    movies=Movie.objects.all()
    ids=random.sample(range(0,len(movies)),6)
    res={}
    data=[]
    cur=0
    for movie in movies:
        if(cur in ids):
            data.append(model_to_dict(movie))
        cur += 1
    res['data']=data
    return HttpResponse(json.dumps(res))

def searches_movies(request):
    type=request.GET['type']
    keywords=request.GET["keywords"]
    print(keywords)
    if(type==4):
        pass

    return HttpResponse("hello")

def update_password(request):
    user = User.objects.filter(username=request.GET['username'], password=request.GET['oldPassword'])
    data = {}
    if (not user.exists()):
        data['success'] = False
        data['error'] = '原密码错误!'
    else:
        data['success'] = True
        user=user[0]
        user.password=request.GET['newPassword']
        user.save()
    return HttpResponse(json.dumps(data))
def get_movie_by_id(request):
    res = {}
    if(cache.has_key(request.GET['id'])):
        movie=cache.get(request.GET['id'])
    else:
        movie=model_to_dict(Movie.objects.get(movieid=request.GET['id']))
        comments = list(Comment.objects.filter(movieid=movie['movieid']).order_by('-commenttime').values())
        for comment in comments:
            comment['nickname']=User.objects.get(userid=comment['userid']).nickname
        movie['shortPopComments']=comments
        itemsimility=ItemSimilarity.objects.get(movieid=movie['movieid']).itemsim.split('/')[:10]
        alsoLikeMovies=[]
        for movie_id in itemsimility:
            alsoLikeMovies.append(movie_id.split(':')[0])
        movie['alsoLikeMovies']=alsoLikeMovies
        cache.set(movie['movieid'],movie,60*60*24)
    res['data']=movie
    return HttpResponse(json.dumps(res))

def get_movie_name_and_img_by_id(request):
    movie = model_to_dict(Movie.objects.get(movieid=request.GET['id']))
    res = {}
    res['data'] = movie
    return HttpResponse(json.dumps(res))

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




