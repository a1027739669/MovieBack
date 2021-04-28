import math
import time
import numpy as np
from MovieWeb.models import *

class CBRec():
    def prepare_user_profile(self, userid):
        user = User.objects.get(userid=userid)
        item_ids=[rating.movieid for rating in Rating.objects.filter(userid=userid)]
        item_ids.extend([rating.movieid for rating in StayRating.objects.filter(userid=userid)])
        items = Movie.objects.in_bulk(item_ids).values()
        ratings = Rating.objects.filter(userid=userid)
        stayratings=StayRating.objects.filter(userid=userid)
        preference = ''
        genres = Genre.objects.all()
        max = -1
        for rating in ratings:
            rectime = rating.ratingtime.split("\n")[0]
            time.strptime(rectime, '%Y-%m-%d %H:%M:%S')
            if (max < (time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (24 * 60 * 60)):
                max = (time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (24 * 60 * 60)
        for stayrating in stayratings:
            rectime = stayrating.ratingtime.split("\n")[0]
            time.strptime(rectime, '%Y-%m-%d %H:%M:%S')
            if (max < (time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (24 * 60 * 60)):
                max = (time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (24 * 60 * 60)
        for genre in genres:
            result = 0.0
            for item in items:
                if (item.genre == None):
                    continue
                if genre.genrename in item.genre.split('/'):
                    for rating in ratings:
                        if rating.movieid == item.movieid:
                            rectime = rating.ratingtime.split("\n")[0]
                            time.strptime(rectime, '%Y-%m-%d %H:%M:%S')

                            result += rating.rating * (((time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (
                                    24 * 60 * 60)) / max)
                    for stayrating in stayratings:
                        if stayrating.movieid == item.movieid:
                            rectime = stayrating.ratingtime.split("\n")[0]
                            time.strptime(rectime, '%Y-%m-%d %H:%M:%S')
                            result += stayrating.rating * (((time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (
                                    24 * 60 * 60)) / max)
            preference += str(genre.id) + ':' + str(result) + '/'
        user.preference = preference
        user.save()

    def prepare_movie_feature(self, movieid):
        movie = Movie.objects.get(movieid=movieid)
        if movie.genre != None:
            movie_genres = movie.genre.split('/')
        else:
            movie_genres = []
        genres = Genre.objects.all()
        feature = ''
        for genre in genres:
            if genre.genrename in movie_genres:
                feature += str(genre.id) + ':' + str(1.0) + '/'
            else:
                feature += str(genre.id) + ':' + str(0) + '/'
        movie.feature = feature
        movie.save()

    def cou_all_user_feature(self):
        users = User.objects.all()
        ratings = Rating.objects.all()
        dic = {}
        genres = Genre.objects.all()
        for rating in ratings:
            if (rating.userid in dic.keys()):
                dic[rating.userid].append(rating)
            else:
                dic[rating.userid] = [rating]
        for user in users:
            print(user.userid)
            item_ids = user.watchitems.split('/')[:-1]  # 去除最后一个回车
            items = Movie.objects.in_bulk(item_ids).values()
            preference = ''
            max = -1
            li = []
            for rating in dic[user.userid]:
                rectime = rating.ratingtime.split("\n")[0]
                time.strptime(rectime, '%Y-%m-%d %H:%M:%S')
                if (max < (time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (24 * 60 * 60)):
                    max = (time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (24 * 60 * 60)
            for genre in genres:
                result = 0.0
                for item in items:
                    if (item.genre == None):
                        continue
                    if genre.genrename in item.genre.split('/'):
                        for rating in dic[user.userid]:
                            if rating.movieid == item.movieid:
                                rectime = rating.ratingtime.split("\n")[0]
                                time.strptime(rectime, '%Y-%m-%d %H:%M:%S')
                                ans = ((time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S'))) / (
                                        24 * 60 * 60)) / max
                                result += rating.rating * ans
                li.extend([str(genre.id), ':', str(result), '/'])
            user.preference = preference.join(li)
            user.save()

    def cosUI(self, userid):
        user = User.objects.get(userid=userid)
        userpre = [eval(x.split(':')[1]) for x in user.preference.split('/')[:-1]]
        item_ids = [eval(x) for x in user.watchitems.split('/')[0:-1]]
        all_items = list(Movie.objects.values_list('movieid', flat=True))
        none_items = Movie.objects.in_bulk(list(set(all_items) - (set(item_ids)))).values()
        result = {}
        for movie in none_items:
            moviefeature = [eval(x.split(':')[1]) for x in movie.feature.split('/')[:-1]]
            Uia = sum(np.array(userpre) * np.array(moviefeature))  # 用杰卡德相似系数
            Ua = math.sqrt(sum([math.pow(one, 2) for one in userpre]))
            Ia = math.sqrt(sum([math.pow(one, 2) for one in moviefeature]))
            if (Ua * Ia != 0):
                result.setdefault(movie.movieid, Uia / (Ua * Ia))
            else:
                result.setdefault(movie.movieid, 0)
        ans = ''
        li = []
        for key, value in result.items():
            li.extend([str(key), ':', str(value), '/'])
        ans = ans.join(li)
        userpreference = UserPreference.objects.get(userid=userid)
        userpreference.userpre = ans
        userpreference.save()

    def recommend(self, userid):
        result = [x.split(':') for x in UserPreference.objects.get(userid=userid).userpre.split('/')][:-1]
        ans = {}  # 存储推荐结果，字典形式
        for x in result:
            ans[x[0]] = x[1]  # 转化为字典结果
        return ans

    def cou_all_ui(self):  # 计算所有用户的偏好
        print(1)
        userpres = [x for x in UserPreference.objects.all()]
        user_pre = {}
        itemids = {}
        print(2)
        users = User.objects.all()
        all_items = list(Movie.objects.values_list('movieid', flat=True))
        none_items = {}
        movie_dict = {}
        movies = Movie.objects.all()
        print(3)
        movid_ferture = {}
        for movie in movies:
            movid_ferture[movie.movieid] = [eval(x.split(':')[1]) for x in movie.feature.split('/')[:-1]]
        for movie in movies:
            movie_dict[movie.movieid] = movie
        for user in users:
            user_pre[user.userid] = [eval(x.split(':')[1]) for x in user.preference.split('/')[:-1]]
            itemids[user.userid] = [eval(x) for x in user.watchitems.split('/')[0:-1]]
        for user in users:
            none_items[user.userid] = list(set(all_items) - set(itemids[user.userid]))

        print('start')
        for userpre in userpres:
            if (userpre.userid % 1000 == 0):
                print(userpre.userid)
            result = {}
            for movie_id in none_items[userpre.userid]:
                Uia = sum(np.array(user_pre[userpre.userid]) * np.array(movid_ferture[movie_id]))  # 用杰卡德相似系数
                Ua = math.sqrt(sum([math.pow(one, 2) for one in user_pre[userpre.userid]]))
                Ia = math.sqrt(sum([math.pow(one, 2) for one in movid_ferture[movie_id]]))
                if (Ua * Ia != 0):
                    result.setdefault(movie_id, Uia / (Ua * Ia))
                else:
                    result.setdefault(movie_id, 0)
            ans = ''  # 用户偏好度 用字符串表
            li = []
            for key, value in result.items():
                li.extend([str(key), ':', str(value), '/'])
            userpre.userpre = ans.join(li)
            userpre.save()
