import json
import os
import math
import time
import operator
from MovieWeb.models import *
class CBRec():
    def prepare_user_profile(self,userid):
        user=User.objects.get(userid=userid)
        item_ids=user.watchitems.split('/')
        items=[]
        for id in item_ids:
            items.append(Movie.objects.get(movie=id))
        already_rating=[]
        for item in items:
            item_genre=item.genre.split('/')
            already_rating.extend(item_genre)
        already_rating=list(set(already_rating))
        ratings=Rating.objects.filter(userid=userid)
        sum=0
        cou=0
        for rating in ratings:
            sum+=rating.rating
            cou+=1
        avg=sum/cou
        genres=Genre.objects.all()
        for genre in genres:
            score_all=0.0
            score_len=0

