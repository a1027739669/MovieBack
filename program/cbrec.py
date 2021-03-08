import json
import os
import math
import time
import operator
import numpy as np
from MovieWeb.models import *
class CBRec():
    K=10
    def prepare_user_profile(self,userid):
        user=User.objects.get(userid=userid)
        item_ids=user.watchitems.split('/')[0:-1] #去除最后一个回车
        items=Movie.objects.in_bulk(item_ids).values()
        ratings=Rating.objects.filter(userid=userid)
        sum=0.0
        cou=0
        preference=''
        for rating in ratings:
            sum+=rating.rating
            cou+=1
        avg=sum/cou
        genres=Genre.objects.all()
        for genre in genres:
            score_all=0.0
            score_len=0
            for item in items:
                if(item.genre==None):
                    continue
                if genre.genrename in item.genre.split('/'):
                    for rating in ratings:
                        if rating.userid==userid and rating.movieid==item.movieid:
                            score_all += rating.rating - avg
                            score_len += 1
            if score_len==0:
                preference+=str(genre.id)+':'+str(0)+'/'
            else:
                preference+= str(genre.id) + ':' + str(round(score_all/score_len,2)) + '/'
        user.preference = preference
        user.save()

    def prepare_movie_feature(self,movieid):
        movie=Movie.objects.get(movieid=movieid)
        if movie.genre!=None:
            movie_genres=movie.genre.split('/')
        else:
            movie_genres = []
        genres=Genre.objects.all()
        feature=''
        for genre in genres:
            if genre.genrename in movie_genres:
                feature += str(genre.id) + ':' + str(1) + '/'
            else:
                feature += str(genre.id) + ':' + str(0) + '/'
        movie.feature = feature
        movie.save()

    def cosUI(self,userid):
        user=User.objects.get(userid=userid)
        userpre=[eval(x.split(':')[1]) for x in user.preference.split('/')[0:-1]]
        item_ids=[eval(x) for x in  user.watchitems.split('/')[0:-1]]
        all_items=list(Movie.objects.values_list('movieid',flat=True))
        none_items=Movie.objects.in_bulk(list(set(all_items)-(set(item_ids)))).values()
        result = {}
        for movie in none_items:
            moviefeature =[eval(x.split(':')[1]) for x in movie.feature.split('/')[0:-1]]
            Uia=sum(np.array(userpre)*np.array(moviefeature)) #用杰卡德相似系数
            Ua=math.sqrt(sum([math.pow(one,2) for one in userpre]))
            Ia=math.sqrt(sum([math.pow(one,2) for one in moviefeature]))
            result.setdefault(movie.movieid,0.0)
            if((Ua*Ia)==0):
                continue
            result[movie.movieid] = Uia / (Ua * Ia)
        result=dict(sorted(result.items(),key=lambda x: x[1],reverse=True))#计算电影偏好排序结果
        ans='' #用户偏好度 用字符串表示
        for key,value in result.items():
            ans+=str(key)+':'+str(value)+'/'
        userpreference=UserPreference.objects.get(userid=userid)
        userpreference.userpre=ans
        userpreference.save()

    def recommend(self,userid):
        result=[x.split(':') for x in UserPreference.objects.get(userid=userid).userpre.split('/')[0:self.K]]
        ans={} #存储推荐结果，字典形式
        for x in result:
            ans.setdefault(eval(x[0]), eval(x[1])) #转化为字典结果
        return ans

















