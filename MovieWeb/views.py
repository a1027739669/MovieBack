from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from back import settings
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
import datetime, time
from .models import *
# Create your views here.
from MovieWeb.models import *
from django.core.mail import send_mail

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

itemBasedCF = ItemBasedCF()
cbrec = CBRec()


def generate_verification_code(isnum):
    ''' 随机生成6位的验证码 '''
    code_list = []
    if isnum == True:
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
    else:
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code


def iter_recommend(id):
    result = itemBasedCF.recommend(id)
    return result


def send_email(request):
    email = request.GET['email']
    user = User.objects.filter(username=email)
    res = {}
    if user.exists():
        res['success'] = False
        res['error'] = '邮箱已经存在'
        return HttpResponse(json.dumps(res))
    try:
        code = generate_verification_code(True)
        send_mail(
            subject='注册验证码',
            message=code,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        cache.set('code' + email, code)
        res['success'] = True
    except:
        res['success'] = False
        res['error'] = '邮箱错误'
        return HttpResponse(json.dumps(res))
    return HttpResponse(json.dumps(res))


def register(request):
    req = json.loads(request.body)
    code = cache.get('code' + req['email'])
    verification = req['verification']
    res = {}
    if code != verification:
        res['success'] = False
        res['error'] = '验证码错误'
        return HttpResponse(json.dumps(res))
    else:
        user = User(img='http://127.0.0.1:8000/media/profile/user.png', nickname=req['username'],
                    password=req['password'], username=req['email'])
        user.save()
        res['success'] = True
        cache.delete('code' + req['email'])
    return HttpResponse(json.dumps(res))


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

    # print('yes')
    # comments= Comment.objects.all()[:20]

    return HttpResponse('测试邮件已发出请注意查收')


def user_login(request):
    req = json.loads(request.body)
    user = User.objects.filter(username=req['username'], password=req['password'])
    res = {}
    if (not user.exists()):
        res['success'] = False
        res['error'] = '用户名或密码错误!'
    else:
        res['success'] = True
        res['data'] = model_to_dict(user[0])
    return HttpResponse(json.dumps(res))


# 获取高评分电影
def get_high_score_movies(request):
    movies = list(Movie.objects.order_by('-score').values()[:10])
    res = {}
    res['data'] = movies
    res['msg'] = '高评分电影'
    return HttpResponse(json.dumps(res))


# 未登录进行随机推荐
def get_recom_movies_unlogin(request):
    movies = Movie.objects.all()
    ids = random.sample(range(0, len(movies)), 6)
    res = {}
    data = []
    cur = 0
    for movie in movies:
        if (cur in ids):
            data.append(model_to_dict(movie))
        cur += 1
    res['data'] = data
    return HttpResponse(json.dumps(res))


# 对登录用户进行推荐
def get_recom_movies(request):
    userid = request.GET['userid']
    user = User.objects.get(userid=userid)
    page = int(request.GET['page'])
    res = {}
    if user.watchitems != None:
        result1 = iter_recommend(userid)
        for key, value in result1.items():  # 将负的相似度全部加上一个偏移改成正值
            result1[key] = (eval(value) + 1) * 0.5
        result2 = cbrec.recommend(userid)
        for key, value in result1.items():
            result1[key] = value * eval(result2[key])  # 将结果乘上内容推荐的偏执值
        ans = dict(sorted(result1.items(), key=operator.itemgetter(1), reverse=True))
        ids = []
        for key in ans.keys():
            ids.append(key)
        data = []
        for id in ids[min(len(ids) - 1, page * 6):min(len(ids) - 1, page * 6 + 6)]:
            data.append(model_to_dict(Movie.objects.get(movieid=id)))
        res['data'] = data
    else:
        movies = list(Movie.objects.order_by('-relesetime').values())
        res = {}
        res['data'] = movies[min(page * 6, len(movies) - 1):min(page * 6 + 6, len(movies) - 1)]
    return HttpResponse(json.dumps(res))


def get_movie_by_id(request):
    res = {}
    if (cache.has_key(request.GET['id'])):
        movie = cache.get(request.GET['id'])
    else:
        movie = model_to_dict(Movie.objects.get(movieid=request.GET['id']))
        comments = list(Comment.objects.filter(movieid=movie['movieid']).order_by('-commenttime').values())
        for comment in comments:
            comment['nickname'] = User.objects.get(userid=comment['userid']).nickname
        movie['shortPopComments'] = comments
        itemsimility = ItemSimilarity.objects.get(movieid=movie['movieid']).itemsim.split('/')[:10]
        alsoLikeMovies = []
        for movie_id in itemsimility:
            alsoLikeMovies.append(movie_id.split(':')[0])
        movie['alsoLikeMovies'] = alsoLikeMovies
        cache.set(movie['movieid'], movie, 60 * 60 * 24)
    res['data'] = movie
    return HttpResponse(json.dumps(res))


def get_also_like(request):
    page = int(request.GET['page'])
    movie = cache.get(request.GET['movieid'])
    itemsimility = ItemSimilarity.objects.get(movieid=movie['movieid']).itemsim.split('/')[page*10:page*10+10]
    alsoLikeMovies = []
    for movie_id in itemsimility:
        alsoLikeMovies.append(movie_id.split(':')[0])
    res={}
    res['alsoLikeMovies']=alsoLikeMovies
    return HttpResponse(json.dumps(res))


def submit_rating(request):  # 提交用户评分
    userid = request.GET['userid']
    if cache.has_key('ratinghistory' + str(userid)):
        cache.delete('ratinghistory' + str(userid))  # 更新了评分就移除缓存

    ratingvalue = request.GET['ratingvalue']
    movieid = request.GET['movieid']
    movie = Movie.objects.get(movieid=movieid)
    user = User.objects.get(userid=userid)
    watch_items = user.watchitems.split('/')[:-1]
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if movieid not in watch_items:
        user.watchitems += str(movieid) + '/'
        rating = Rating(rating=ratingvalue, movieid=movieid, userid=userid, ratingtime=str(now_time))
        rating.save()
        cbrec.prepare_user_profile(userid)
        cbrec.cosUI(userid)
        user.save()
        movie.vote += 1
    else:
        rating = Rating.objects.get(userid=userid, movieid=movieid)
        movie.all_score -= int(rating.rating)
        rating.rating = int(ratingvalue)
        rating.ratingtime = str(now_time)
        rating.save()
        cbrec.prepare_user_profile(userid)
        cbrec.cosUI(userid)
    movie.all_score += int(ratingvalue)
    movie.score = round(movie.all_score / movie.vote)
    movie.save()
    return HttpResponse("成功")


def submit_comment(request):
    movieid = request.GET['movieid']
    commenttime = request.GET['commenttime']
    content = request.GET['content']
    userid = request.GET['userid']
    comment = Comment(commenttime=commenttime, content=content, userid=userid, movieid=movieid)
    comment.save()
    if cache.has_key(movieid):  # 删除缓存
        cache.delete(movieid)
    if cache.has_key('commenthistory' + str(userid)):
        cache.delete('commenthistory' + str(userid))  # 删除缓存
    return HttpResponse("hello")


def get_rating_list(request):  # 获取用户评分记录，即浏览记录
    userid = request.GET['userid']
    res = {}
    if cache.has_key('ratinghistory' + str(userid)):
        ratings = cache.get('ratinghistory' + str(userid))
    else:
        ratings = list(Rating.objects.filter(userid=userid).order_by('-ratingtime').values())
        for rating in ratings:
            rating['moviename'] = Movie.objects.get(movieid=rating['movieid']).name
        cache.set('ratinghistory' + str(userid), ratings)
    res['data'] = ratings
    return HttpResponse(json.dumps(res))


def get_comment_list(request):  # 获取用户评论记录
    userid = request.GET['userid']
    res = {}
    if cache.has_key('commenthistory' + str(userid)):
        comments = cache.get('commenthistory' + str(userid))
    else:
        comments = list(Comment.objects.filter(userid=userid).order_by('-commenttime').values())
        for comment in comments:
            comment['moviename'] = Movie.objects.get(movieid=comment['movieid']).name
        cache.set('commenthistory' + str(userid), comments)
    res['data'] = comments
    return HttpResponse(json.dumps(res))


def delete_comment(request):  # 用户删除一条评论
    commentid = request.GET['commentid']
    comment = Comment.objects.get(commentid=commentid)  # 获取评论
    movie = Movie.objects.get(movieid=comment.movieid)  # 获取评论相关联的电影
    user = User.objects.get(userid=comment.userid)  # 获取评论相关联的用户
    comment.delete()
    if cache.has_key(movie.movieid):  # 删除缓存
        cache.delete(movie.movieid)
    comments = cache.get('commenthistory' + str(user.userid))  # 获取缓存准备更新
    for comment in comments:
        if str(comment['commentid']) == str(commentid):
            comments.remove(comment)  # 移除删除的评论
            break
    cache.set('commenthistory' + str(user.userid), comments)  # 重新设置缓存
    res = {}
    res['data'] = comments
    return HttpResponse(json.dumps(res))


def searches_movies(request):
    keywords = request.GET["keywords"]
    print(keywords)
    limit = request.GET["limit"]
    offset = request.GET["offset"]
    sort = request.GET['sort']
    year = request.GET['year']
    region = request.GET['region']
    res = {}
    movies = Movie.objects.filter(genre__icontains=keywords).order_by('movieid')
    if sort != '':
        movies = movies.order_by('-' + sort)
    if year != '':
        movies = movies.filter(year__icontains=year)
    if region != '':
        movies = movies.filter(region__icontains=region)
    paginator = Paginator(movies, limit)
    data = list(paginator.page(int(offset) / int(limit) + 1).object_list.values())
    if len(data) == 0:
        res['success'] = False
        res['error'] = '无符合条件的数据!'
    else:
        res['data'] = data
    return HttpResponse(json.dumps(res))


def searches_movie_by_keyword(request):
    keywords = request.GET["keywords"]
    limit = request.GET["limit"]
    offset = request.GET["offset"]
    res = {}
    # 全字段模糊查询
    movies = Movie.objects.filter(Q(actors__icontains=keywords) | Q(alias__icontains=keywords) | Q(
        director__icontains=keywords) | Q(genre__icontains=keywords) | Q(language__icontains=keywords) | Q(
        name__icontains=keywords) | Q(region__icontains=keywords) | Q(relesetime__icontains=keywords) | Q(
        score__icontains=keywords) | Q(storyline__icontains=keywords)).order_by('-score')
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
        user = user[0]
        user.password = request.GET['newPassword']
        user.save()
    return HttpResponse(json.dumps(data))


def get_movie_name_and_img_by_id(request):
    movie = model_to_dict(Movie.objects.get(movieid=request.GET['id']))
    res = {}
    res['data'] = movie
    return HttpResponse(json.dumps(res))


def download():
    movies = Movie.objects.all()
    for movie in movies:
        spi.download_image(movie.movieid)


def cou_sim_mutex():
    itemBasedCF.load_data()
    itemBasedCF.data_transfer()
    itemBasedCF.similarity()
