import uuid
import json
from django.db.models import Q
from back import settings
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.cache import cache
from program.itemrec import *
from program.cbrec import *
from django.core.serializers import serialize, deserialize
from program import spi
import random
import datetime
# Create your views here.
from MovieWeb.models import *
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password

local_file_url = 'http://127.0.0.1:8000/media/'
local_file_path = 'C:/Users/Komorebi/Desktop/back/media/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

itemBasedCF = ItemBasedCF()
cbrec = CBRec()


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)


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


def register(request):  # 注册
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
        cache.set('userslen', int(cache.get('userslen')) + 1, 60 * 60 * 24 * 365)

    return HttpResponse(json.dumps(res))


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


def user_login(request):
    req = json.loads(request.body)
    user = User.objects.filter(username=req['username'], password=req['password'])
    res = {}
    if (not user.exists()):
        res['success'] = False
        res['error'] = '用户名或密码错误!'
    else:
        res['success'] = True
        if not UserPreference.objects.filter(userid=user[0].userid).exists():
            userpreference = UserPreference(userid=user[0].userid)
            userpreference.save()
        res['data'] = model_to_dict(user[0])
    return HttpResponse(json.dumps(res))


def set_watch(request):
    return HttpResponse('hello')


def get_favorite(request):
    userid = request.GET['userid']
    favorites = list(Favorite.objects.filter(userid=userid).values())
    res = {}
    res['favorites'] = favorites
    res['first'] = favorites[0]
    movieids = CollectMovie.objects.filter(favoriteid=favorites[0]['favoriteid'])
    movies = []
    for item in movieids:
        movies.append(change_movie(model_to_dict(Movie.objects.get(movieid=item.movieid))))
    res['movies'] = movies
    return HttpResponse(json.dumps(res))


def get_favorite_movies(request):
    favorite = Favorite.objects.get(favoriteid=request.GET['favoriteid'])
    movieids = CollectMovie.objects.filter(favoriteid=favorite.favoriteid)
    movies = []
    for item in movieids:
        movies.append(change_movie(model_to_dict(Movie.objects.get(movieid=item.movieid))))
    res = {}
    res['favorite'] = model_to_dict(favorite)
    res['movies'] = movies
    return HttpResponse(json.dumps(res))


def new_favorite(request):
    favoriteid = int(round(time.time() * 1000))
    userid = request.GET["userid"]
    favoritename = request.GET["favoritename"]
    favorite = Favorite(favoriteid=favoriteid, favoritename=favoritename, userid=userid)
    favorite.save()
    res = {}
    res['favoriteid'] = favoriteid
    return HttpResponse(json.dumps(res))


def update_favorite(request):
    favoriteid = request.GET["favoriteid"]
    favoritename = request.GET["favoritename"]
    favorite = Favorite.objects.get(favoriteid=favoriteid)
    favorite.favoritename = favoritename
    favorite.save()
    res = {}
    res['success'] = True
    return HttpResponse(json.dumps(res))


def delete_favorite(request):
    favoriteid = request.GET['favoriteid']
    Favorite.objects.filter(favoriteid=favoriteid).delete()
    CollectMovie.objects.filter(favoriteid=favoriteid).delete()
    StayRating.objects.filter(favoriteid=favoriteid).delete()
    res = {}
    res['success'] = True
    return HttpResponse(json.dumps(res))


def add_movie_to_favorite(request):
    favoriteid = request.GET["favoriteid"]
    movieid = request.GET["movieid"]
    if not CollectMovie.objects.filter(favoriteid=favoriteid, movieid=movieid).exists():
        collectmovie = CollectMovie(movieid=movieid, favoriteid=favoriteid)
        collectmovie.save()
    res = {}
    res['success'] = True
    return HttpResponse(json.dumps(res))


def get_cur_movies(request):
    movies = Movie.objects.all().order_by('-relesetime')[:3]
    data = []
    for movie in movies:
        data.append(model_to_dict(movie))
    res = {}
    res['data'] = change_movies(data)
    return HttpResponse(json.dumps(res))


def upload_user_img(request):
    img = request.FILES.get('file')
    img_name = str(uuid.uuid1())
    img_path = local_file_path + 'profile/' + img_name + '.jpg'
    with open(img_path, 'wb') as f:
        for chunk in img.chunks():
            f.write(chunk)
    res = {}
    res['url'] = local_file_url + 'profile/' + img_name + '.jpg'
    return HttpResponse(json.dumps(res))


def sava_user_img_to_db(request):
    user = User.objects.get(userid=request.GET['userid'])
    url = request.GET['url']
    user.img = url
    user.save()
    res = {}
    res['userimg'] = url
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


def update_user_profile(request):
    req = json.loads(request.body)
    user = User.objects.get(userid=req['userid'])
    user.img = req['img']
    user.local = req['local']
    user.selfnote = req['selfnote']
    user.nickname = req['nickname']
    user.save()
    res = {}
    res['success'] = True
    return HttpResponse(json.dumps(res))


def get_rating_list(request):  # 获取用户评分记录，即浏览记录
    userid = request.GET['userid']
    res = {}
    if cache.has_key('ratinghistory' + str(userid)):
        ratings = cache.get('ratinghistory' + str(userid))
    else:
        ratings = list(Rating.objects.filter(userid=userid).order_by('-ratingtime').values())
        for rating in ratings:
            rating['moviename'] = Movie.objects.get(movieid=rating['movieid']).name
        cache.set('ratinghistory' + str(userid), ratings, 60 * 60 * 24)
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
        cache.set('commenthistory' + str(userid), comments, 60 * 60 * 24)
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
    cache.set('commenthistory' + str(user.userid), comments, 60 * 60 * 24)  # 重新设置缓存
    res = {}
    res['data'] = comments
    cache.set('commentslen', int(cache.get('commentslen')) - 1, 60 * 60 * 24 * 365)
    return HttpResponse(json.dumps(res))


def get_high_score_movies(request):
    movies = list(Movie.objects.order_by('-score').values()[:10])
    res = {}
    res['data'] = movies
    res['msg'] = '高评分电影'
    res = {}
    res['data'] = movies
    return HttpResponse(json.dumps(res))


def get_persons(request):
    persons = list(Person.objects.order_by('personid').values()[:10])
    res = {}
    res['data'] = persons
    return HttpResponse(json.dumps(res))


def get_recom_movies_unlogin(request):
    movies = Movie.objects.all()
    ids = random.sample(range(0, len(movies)), 10)
    res = {}
    data = []
    cur = 0
    for movie in movies:
        if (cur in ids):  # 获取10个随机电影加入结果
            data.append(model_to_dict(movie))
        cur += 1
    res['data'] = change_movies(data)
    return HttpResponse(json.dumps(res))


def get_recom_movies(request):
    userid = request.GET['userid']
    user = User.objects.get(userid=userid)
    page = int(request.GET['page'])
    res = {}
    if user.watchitems != None:
        result1 = iter_recommend(userid)
        result2 = cbrec.recommend(userid)
        for key, value in result1.items():
            result1[key] = value * eval(result2[key])  # 将结果乘上内容推荐的偏执值
        ans = dict(sorted(result1.items(), key=operator.itemgetter(1), reverse=True))
        ids = []
        for key in ans.keys():
            ids.append(key)
        data = []
        for id in ids[min(len(ids) - 1, page * 10):min(len(ids) - 1, page * 10 + 10)]:
            data.append(model_to_dict(Movie.objects.get(movieid=id)))
        res['data'] = change_movies(data)
    else:
        movies = list(Movie.objects.order_by('-relesetime').values())
        res = {}
        res['data'] = change_movies(movies[min(page * 10, len(movies) - 1):min(page * 10 + 10, len(movies) - 1)])
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
        movie_actor = []
        if movie['actorid'] != None:
            actors = movie['actorid'].split("|")
            for actor in actors:
                actorli = actor.split(':')
                x = {'actorname': actorli[0], 'actorid': actorli[1]}
                movie_actor.append(x)
        movie['actor_li'] = movie_actor
        cache.set(movie['movieid'], movie, 60 * 60 * 24)
    if (not ItemSimilarity.objects.filter(movieid=movie['movieid']).exists()):
        itemsimilarity = ItemSimilarity(movieid=movie['movieid'])
        itemsimilarity.save()
    res['data'] = change_movie(movie)
    return HttpResponse(json.dumps(res))


def cou_stay_time(request):  # 根据用户停留时间改变用户偏好度
    startTime = request.GET['startTime']
    endTime = request.GET['endTime']
    userid = request.GET['userid']
    if userid != '':
        movieid = request.GET['movieid']
        time.strptime(startTime, '%Y-%m-%d %H:%M:%S')
        time1 = time.mktime(time.strptime(startTime, '%Y-%m-%d %H:%M:%S'))
        time.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        time2 = time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S'))
        if (time2 - time1) >= 60:
            rating = 5
        else:
            rating = (time2 - time1) / 60.0 * 5
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        movieRating = StayRating(movieid=movieid, rating=rating, ratingtime=str(now_time), userid=userid)
        movieRating.save()
        cbrec.prepare_user_profile(userid)
        cbrec.cosUI(userid)
    res = {}
    res['success'] = True
    return HttpResponse(json.dumps(res))


def get_also_like(request):
    page = int(request.GET['page'])
    movie = cache.get(request.GET['movieid'])
    itemsimility = ItemSimilarity.objects.get(movieid=movie['movieid']).itemsim.split('/')[page * 10:page * 10 + 10]
    alsoLikeMovies = []
    for movie_id in itemsimility:
        alsoLikeMovies.append(movie_id.split(':')[0])
    res = {}
    res['alsoLikeMovies'] = alsoLikeMovies
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
    movie.score = round(movie.all_score / movie.vote, 1)
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
    cache.set('commentslen', int(cache.get('commentslen')) + 1, 60 * 60 * 24 * 365)
    return HttpResponse("hello")


def get_person_by_id(request):
    res = {}
    person = model_to_dict(Person.objects.get(personid=request.GET['id']))
    parMovies = []
    person['imgfile'] = None
    movies = Movie.objects.filter(Q(actors__icontains=person['name']) | Q(director__icontains=person['name']))
    for movie in movies:
        parMovies.append(movie.movieid)
    person['parMovies'] = parMovies
    res['data'] = person
    return HttpResponse(json.dumps(res))


def searches_movies(request):
    keywords = request.GET["keywords"]
    limit = request.GET["limit"]
    offset = request.GET["offset"]
    sort = request.GET['sort']
    year = request.GET['year']
    region = request.GET['region']
    res = {}
    movies = Movie.objects.filter(genre__icontains=keywords).order_by('movieid')
    if sort != '':
        movies = movies.order_by('-' + sort)
    if year != '' and year != '全部':
        movies = movies.filter(year__icontains=year)
    if region != '' and region != '全部':
        movies = movies.filter(region__icontains=region)
    paginator = Paginator(movies, limit)
    data = list(paginator.page(int(offset) / int(limit) + 1).object_list.values())
    if len(data) == 0:
        res['success'] = False
        res['error'] = '无符合条件的数据!'
    else:
        res['data'] = data
    return HttpResponse(json.dumps(res))


def del_collect_movie(request):
    favoriteid = request.GET['favoriteid']
    movieid = request.GET["movieid"]
    CollectMovie.objects.filter(favoriteid=favoriteid, movieid=movieid).delete()
    StayRating.objects.filter(movieid=movieid,favoriteid=favoriteid).delete()
    res = {}
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


def searches_person_by_keyword(request):
    keywords = request.GET["keywords"]
    limit = request.GET["limit"]
    offset = request.GET["offset"]
    res = {}
    # 全字段模糊查询
    persons = Person.objects.filter(
        Q(name__icontains=keywords) | Q(birthday__icontains=keywords) | Q(birthplace__icontains=keywords) | Q(
            blog__icontains=keywords) | Q(constellation__icontains=keywords) | Q(
            nameen__icontains=keywords) | Q(namezh__icontains=keywords) | Q(profession__icontains=keywords) | Q(
            sex__icontains=keywords)).order_by('-personid')
    paginator = Paginator(persons, limit)
    data = list(paginator.page(int(offset) / int(limit) + 1).object_list.values())
    if len(data) == 0:
        res['success'] = False
        res['error'] = '无符合条件的数据!'
    else:
        res['data'] = data
    return HttpResponse(json.dumps(res))


def get_movie_name_and_img_by_id(request):
    movie = model_to_dict(Movie.objects.get(movieid=request.GET['id']))
    res = {}
    res['data'] = change_movie(movie)
    return HttpResponse(json.dumps(res))


def download():
    movies = Movie.objects.all()
    for movie in movies:
        spi.download_image(movie.movieid)


def save_message(request):
    req = json.loads(request.body)
    now_time = datetime.datetime.now().strftime("%Y-%m-%d")
    chatrecord = ChatRecord(uid=req['userid'], nickname=req['nickname'], content=req['content'], img=req['img'],
                            type=req['type'], date=now_time)
    chatrecord.save()
    res = {}
    res['success'] = True
    return HttpResponse(json.dumps(res))


def get_meaaage(request):
    cur_date = datetime.datetime.now().date()
    week = cur_date - datetime.timedelta(weeks=1)
    res = {}
    # 查询前一周数据
    obj_list = list(ChatRecord.objects.filter(date__gte=week, date__lte=cur_date).values())
    res['messageList'] = obj_list
    return HttpResponse(json.dumps(res))


def cou_sim_mutex():
    itemBasedCF.load_data()
    itemBasedCF.data_transfer()
    itemBasedCF.similarity()


def change_movie(movie):
    movie['imgfile'] = None
    return movie


def change_movies(movies):
    for movie in movies:
        movie['imgfile'] = None
    return movies


def has_key(request):
    pass


def get(request):
    pass


def set(request):
    pass
