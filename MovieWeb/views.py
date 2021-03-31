from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
import time
from program.itemrec import *
from program.cbrec import *
from program import spi
import random
import datetime,time
from .models import *
# Create your views here.
from MovieWeb.models import*
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

file_path="data/rating.csv"
itemBasedCF = ItemBasedCF()
cbrec=CBRec()
# itemBasedCF.load_data(file_path)
# itemBasedCF.data_transfer()
# itemBasedCF.similarity()

def iter_recommend(id):
    result={}
    result=itemBasedCF.recommend(id)
    return result

def set_watch(request):
    # movies=Movie.objects.all()
    # for movie in movies:
    #     cou=0
    #     all_score=0
    #     ratings=Rating.objects.filter(movieid=movie.movieid)
    #     for rating in ratings:
    #         cou+=1
    #         all_score+=int(rating.rating)
    #     if cou==0:
    #         movie.score=0
    #         movie.all_score=all_score
    #         movie.vote=0
    #     else:
    #         movie.score=round(all_score/cou,1)
    #         movie.all_score=all_score
    #         movie.vote=cou
    #     movie.save()
    #     print(movie.movieid)
    # cou_sim_mutex()


    return HttpResponse("hello")

def user_login(request):
    req=json.loads(request.body)
    user=User.objects.filter(username=req['username'],password=req['password'])
    res={}
    if(not user.exists()):
        res['success']=False
        res['error']='用户名或密码错误!'
    else:
        res['success']=True
        res['data']=model_to_dict(user[0])
    return HttpResponse(json.dumps(res))

#获取高评分电影
def get_high_score_movies(request):
    movies=list(Movie.objects.order_by('-score').values()[:10])
    res={}
    res['data']=movies
    res['msg']='高评分电影'
    return HttpResponse(json.dumps(res))

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

#对登录用户进行推荐
def get_recom_movies(request):
    userid=request.GET['userid']
    result1=iter_recommend(userid)
    for key,value in result1.items(): #将负的相似度全部加上一个偏移改成正值
        result1[key]=(eval(value)+1)*0.5
    result2=cbrec.recommend(userid)
    for key,value in result1.items():
        result1[key]=value*eval(result2[key])#将结果乘上内容推荐的偏执值
    ans=dict(sorted(result1.items(), key=operator.itemgetter(1), reverse=True)[0:30])
    ids=[]
    for key in ans.keys():
        ids.append(key)
    res={}
    data=[]
    for id in ids[:6]:
        data.append(model_to_dict(Movie.objects.get(movieid=id)))
    res['data']=data
    return HttpResponse(json.dumps(res))

def submit_rating(request): #提交用户评分
    userid=request.GET['userid']
    ratingvalue=request.GET['ratingvalue']
    movieid=request.GET['movieid']
    movie=Movie.objects.get(movieid=movieid)
    user=User.objects.get(userid=userid)
    watch_items=user.watchitems.split('/')[:-1]
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if movieid not in watch_items:
        user.watchitems+=str(movieid)+'/'
        rating=Rating(rating=ratingvalue,movieid=movieid,userid=userid,ratingtime=str(now_time))
        rating.save()
        cbrec.prepare_user_profile(userid)
        cbrec.cosUI(userid)
        user.save()
        movie.vote+=1
    else:
        rating=Rating.objects.get(userid=userid,movieid=movieid)
        movie.all_score-=int(rating.rating)
        rating.rating=int(ratingvalue)
        rating.ratingtime=str(now_time)
        rating.save()
        cbrec.prepare_user_profile(userid)
        cbrec.cosUI(userid)
    movie.all_score += int(ratingvalue)
    movie.score = round(movie.all_score / movie.vote)
    movie.save()
    return HttpResponse("成功")

def searches_movies(request):
    type=request.GET['type']
    keywords=request.GET["keywords"]
    limit=request.GET["limit"]
    offset=request.GET["offset"]
    sort=request.GET['sort']
    res={}
    #根据名称进行查询
    if(type=='3'):
        movies=Movie.objects.filter(name__icontains=keywords).order_by('-'+sort)
    elif type=='10':
        movies = Movie.objects.filter(genre__icontains=keywords).order_by('-'+sort)
    elif type=='16':
        movies = Movie.objects.filter(alias__icontains=keywords).order_by('-'+sort)
    elif type =='7':
        movies = Movie.objects.filter(director__icontains=keywords).order_by('-'+sort)
    elif type =='9':
        movies = Movie.objects.filter(actors__icontains=keywords).order_by('-'+sort)
    elif type =='10':
        movies = Movie.objects.filter(genre__icontains=keywords).order_by('-'+sort)
    elif type =='12':
        movies = Movie.objects.filter(region__icontains=keywords).order_by('-'+sort)
    elif type =='14':
        movies = Movie.objects.filter(language__icontains=keywords).order_by('-'+sort)
    elif type =='6':
        movies = Movie.objects.filter(year__icontains=keywords).order_by('-'+sort)
    else:
        movies = Movie.objects.filter(score__gte=keywords).order_by('-' + sort)
    paginator = Paginator(movies, limit)
    data = list(paginator.page(int(offset) / int(limit) + 1).object_list.values())
    if len(data) == 0:
        res['success'] = False
        res['error'] = '无符合条件的数据!'
    else:
        res['data'] = data
    return HttpResponse(json.dumps(res))

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


def download():
    movies=Movie.objects.all()
    for movie in movies:
        spi.download_image(movie.movieid)

def cou_sim_mutex():
    itemBasedCF.load_data()
    itemBasedCF.data_transfer()
    itemBasedCF.similarity()




