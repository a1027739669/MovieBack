import math
import time
import operator
from MovieWeb.models import *
class ItemBasedCF:
    def __init__(self):
        self.N = {}  # 记录每部电影被多少用户看过
        self.W = {}  # 相似度矩阵
        self.data={}
        self.train = {}#训练集
        self.test = {}#测试集
        self.k = 300 #最相似的K部电影
        self.n = 100 #返回n个结果
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
            li=[]
            for key, value in itemsim_dict.items():
                li.extend([str(key) , ':' , str(value) , '/'])
            itemsim=itemsim.join(li)
            itemsimilarity = ItemSimilarity.objects.get(movieid=i)
            itemsimilarity.itemsim = itemsim
            itemsimilarity.save()
            print(cou)
            cou+=1
        print('计算相似度矩阵完成...')

    def recommend(self, userid):
        """
        推荐函数
        """
        # print('开始向用户{}推荐...'.format(userid))
        user = User.objects.get(userid=userid)
        ans = {}
        item_ids = user.watchitems.split('/')[0:-1] # 看过的电影
        for i in item_ids:
            result = [x.split(':') for x in ItemSimilarity.objects.get(movieid=i).itemsim.split('/')[0:self.k]]
            for x in result:
                if(x[0] in item_ids):
                    continue
                # ans[x[0]]=x[1]
                ans.setdefault(x[0],0.0)
                ans[x[0]]+=float(x[1])*Rating.objects.get(movieid=i,userid=userid).rating
        return dict(sorted(ans.items(), key=operator.itemgetter(1), reverse=True)[0:self.n])
