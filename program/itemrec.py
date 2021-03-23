import json
import os
import math
import time
import operator
from MovieWeb.models import *
# file_path="../data/rating.csv"
class ItemBasedCF:
    def __init__(self):
        self.N = {}  # 记录每部电影被多少用户看过
        self.W = {}  # 相似度矩阵
        self.data={}
        self.train = {}#训练集
        self.test = {}#测试集
        self.k = 30 #最相似的K部电影
        self.n = 10 #返回n个结果
        self.R={}#记录对电影i和j感兴趣的评分
        self.M=9
        self.ram=3
        self.seed=47
        self.rectime={} #对电影评价时间
    def load_data(self):
        """
        加载数据
        """
        print('正在加载数据... ')

        # with open(file_path, "r",encoding="utf8") as file:
        #     for i, line in enumerate(file, 0):
        #         if i != 0:  # 跳过第一行
        #             line = line.strip('\r')
        #             _, userid, itemid, rating,rectime = line.split(',')
        #             self.train.setdefault(userid, {})
        #             self.rectime.setdefault(userid,{})
        #             self.train[userid][itemid]=rating
        #             rectime=rectime.split("\n")[0]
        #             time.strptime(rectime, '%Y-%m-%d %H:%M')#将日期转换为时间戳
        #             self.rectime[userid][itemid] =(time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M')))/(24*60*60)#将日期转换为时间戳
        ratings=Rating.objects.all()
        for rating in ratings:
            self.train.setdefault(rating.userid, {})
            self.rectime.setdefault(rating.userid,{})
            self.train[rating.userid][rating.movieid]=rating.rating
            rectime=rating.ratingtime.split("\n")[0]
            time.strptime(rectime, '%Y-%m-%d %H:%M:%S')#将日期转换为时间戳
            self.rectime[rating.userid][rating.movieid] =(time.mktime(time.strptime(rectime, '%Y-%m-%d %H:%M:%S')))/(24*60*60)#将日期转换为时间戳
        print('加载完成...')


    def data_transfer(self):
        for userid,item_ratings in self.train.items():
            items = list(item_ratings.keys()) #电影集合
            ratings=[int(x) for x in item_ratings.values()]#评分集合
            total=sum(ratings)
            for i in range(len(ratings)):
                rating=ratings[i]-total/len(ratings)  #归一化评分
                self.train[userid][items[i]]=rating


    def similarity(self):
        """
        计算相似度函数
        """
        cou=1
        print('开始计算物品相似度...')
        # if os.path.exists('data/item_sim.json'):
        #     print('从文件加载物品相似度...')
        #     self.W=json.load(open('data/item_sim.json','r'))
        #     print("相似度加载完成...")
        # else:
        #     for userid, item_ratings in self.train.items():
        #         items=list(item_ratings.keys())
        #         for i in items:
        #             self.R.setdefault(i,[])
        #             self.R[i].append(userid)
        #     for i,i_users in self.R.items(): #计算i和j的余弦相似度
        #         for j,j_users in self.R.items():
        #             if i!=j:
        #                 self.W.setdefault(i, {})
        #                 self.W[i].setdefault(j,0)
        #                 uids=list(set(i_users)&set(j_users))
        #                 iratings=[]
        #                 jratings=[]
        #                 uratings=[]
        #                 for id in uids:
        #                     time_factor=math.log(math.e+math.fabs(self.rectime[id][i]-self.rectime[id][j]))  #加入时间因子
        #                     iratings.append(self.train[id][i]**2) #对i的评分
        #                     jratings.append(self.train[id][j]**2)  #对j的评分
        #                     uratings.append(self.train[id][i]*self.train[id][j]*(1/time_factor))
        #                 self.W[i][j]=sum(uratings)/(math.sqrt(sum(iratings))*math.sqrt(sum(jratings)))
        #     json.dump(self.W, open('data/item_sim.json', 'w'))

        for userid, item_ratings in self.train.items():
            items=list(item_ratings.keys())
            for i in items:
                self.R.setdefault(i,[])
                self.R[i].append(userid)
        for i,i_users in self.R.items(): #计算i和j的余弦相似度
            itemsim_dict={}
            itemsim=''
            for j,j_users in self.R.items():
                if i!=j:
                    itemsim_dict.setdefault(j,0.0)
                    uids=list(set(i_users)&set(j_users))
                    iratings=[]
                    jratings=[]
                    uratings=[]
                    for id in uids:
                        time_factor=math.log(math.e+math.fabs(self.rectime[id][i]-self.rectime[id][j]))  #加入时间因子
                        iratings.append(self.train[id][i]**2) #对i的评分
                        jratings.append(self.train[id][j]**2)  #对j的评分
                        uratings.append(self.train[id][i]*self.train[id][j]*(1/time_factor))
                    if(math.sqrt(sum(iratings))*math.sqrt(sum(jratings))!=0):
                        itemsim_dict[j]=sum(uratings)/(math.sqrt(sum(iratings))*math.sqrt(sum(jratings)))
                    else:
                        itemsim_dict[j]=-1
            itemsim_dict = dict(sorted(itemsim_dict.items(), key=lambda x: x[1], reverse=True))
            for key, value in itemsim_dict.items():
                itemsim.join([str(key) , ':' , str(value) , '/'])
            itemsimilarity = ItemSimilarity.objects.get(movieid=i)
            itemsimilarity.itemsim = itemsim
            itemsimilarity.save()
            print(cou)
            cou+=1
        print('计算相似度矩阵完成...')

            # for userid, item_ratings in self.train.items():
            #     items = [x[0] for x in item_ratings]  #用户看过的电影IDs
            #     for i in items:
            #         self.N.setdefault(i, 0)
            #         self.N[i] += 1  # 用户对电影i感兴趣
            #         for j in items:
            #             if i != j:
            #                 self.W.setdefault(i, {})
            #                 self.W[i].setdefault(j, 0)
            #                 self.W[i][j] += 1  # 用户对i电影和j电影感兴趣
            # for i, j_cnt in self.W.items():
            #     for j, cnt in j_cnt.items():
            #         self.W[i][j] = self.W[i][j] / (self.N[i] * self.N[j]) ** 0.5  # 电影i和j的相似度
            # json.dump(self.W, open('data/item_sim.json', 'w'))
            # print('计算相似度矩阵完成...')

    def recommend(self, userid):
        """
        推荐函数
        """
        # print('开始向用户{}推荐...'.format(user))
        # result= {}
        # watched_items =list(self.train[user].keys()) #遍历出来是看过的电影
        # for i in watched_items:
        print('开始向用户{}推荐...'.format(userid))
        user = User.objects.get(userid=userid)
        result = {}
        ans = {}
        item_ids = user.watchitems.split('/')[0:-1] # 看过的电影
        for i in item_ids:
            result = [x.split(':') for x in ItemSimilarity.objects.get(movieid=i).itemsim.split('/')[0:self.k]]
            for x in result:
                if(x[0] in item_ids):
                    continue
                ans[x[0]]=x[1]
        return dict(sorted(ans.items(), key=operator.itemgetter(1), reverse=True)[0:self.n])
            # for j, similarity in sorted(self.W[i].items(), key=lambda x: x[1], reverse=True)[0:self.k]:
            #     if j not in watched_items:
            #         result.setdefault(j, 0.)
            #         result[j] += float(self.train[user][i]) * similarity
        # return dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True)[0:self.n])

