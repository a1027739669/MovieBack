# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.html import format_html

class Comment(models.Model):
    commentid = models.BigIntegerField(primary_key=True,verbose_name='id')
    commenttime = models.CharField(max_length=255, blank=True, null=True,verbose_name='评论时间')
    content = models.TextField(blank=True, null=True,verbose_name='评论内容')
    movieid = models.BigIntegerField(blank=True, null=True,verbose_name='电影id')
    userid = models.BigIntegerField(blank=True, null=True,verbose_name='用户id')
    img = models.TextField(blank=True, null=True, verbose_name='用户头像')
    class Meta:
        managed = True
        db_table = 'comment'
        verbose_name = '评论'  # 后台显示的表名
        verbose_name_plural = '评论管理'


class Genre(models.Model):
    id = models.BigIntegerField(primary_key=True)
    genrename = models.CharField(max_length=255, blank=True, null=True,verbose_name='类型名')
    def __str__(self):
        return self.genrename
    class Meta:
        managed = True
        db_table = 'genre'
        verbose_name = '类型'  # 后台显示的表名
        verbose_name_plural = '类型管理'  # 后台显示的表名复数 英语复数是加s 这里我们写死为 要显示的表名



class Person(models.Model):
    personid = models.BigIntegerField(primary_key=True, verbose_name='id')
    name = models.TextField(blank=True, null=True,verbose_name='姓名')
    nameen = models.TextField(blank=True, null=True,verbose_name='英文名')
    birthday = models.CharField(max_length=255,blank=True, null=True,verbose_name='生日')
    birthplace = models.CharField(max_length=255, blank=True, null=True,verbose_name='出生地')
    blog = models.TextField(blank=True, null=True,verbose_name='个人简介')
    constellation = models.CharField(max_length=255, blank=True, null=True,verbose_name='星座')
    profession = models.TextField(blank=True, null=True,verbose_name='职业')
    sex = models.CharField(max_length=255, blank=True, null=True,verbose_name='性别',choices=(('男', '男'), ('女', '女')))
    img=models.TextField(blank=True, null=True,verbose_name='图片')
    imgfile=models.ImageField(blank=True,null=True,upload_to='personimg/',verbose_name='图片文件')

    def __str__(self):
        return self.name
    def image_img(self):
        # 这里添加一个防空判断
        if not self.img:
            return '无'
        return format_html("""<div οnclick='$(".my_set_image_img").hide();$(this).next().show();'><img src='{}' style='width:50px;height:50px;' ></div><div class='my_set_image_img' οnclick="$('.my_set_image_img').hide()" style="z-index:9999;position:fixed; left: 100px; top:100px;display:none;"><img src='{}' style='width:500px; height:500px;'></div>""",self.img, self.img)

    image_img.short_description = '图片'
    class Meta:
        managed = True
        db_table = 'person'
        verbose_name = '演员'  # 后台显示的表名
        verbose_name_plural = '演员管理'

class Movie(models.Model):
    movieid = models.BigIntegerField(primary_key=True,verbose_name='id')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='电影名')
    actorid = models.TextField(blank=True, null=True,verbose_name='演员id')
    alias = models.CharField(max_length=255, blank=True, null=True,verbose_name='别名')
    director = models.CharField(max_length=255, blank=True, null=True,verbose_name='导演')
    directorid = models.TextField(blank=True, null=True,verbose_name='导演id')
    genre = models.CharField(max_length=255, blank=True, null=True,verbose_name='类型')
    language = models.CharField(max_length=255, blank=True, null=True,verbose_name='语言')
    minus = models.BigIntegerField(blank=True, null=True,verbose_name='时长')
    region = models.CharField(max_length=255, blank=True, null=True,verbose_name='地区')
    relesetime = models.CharField(max_length=255, blank=True, null=True,verbose_name='发行时间')
    year= models.CharField(max_length=255, blank=True, null=True)
    score = models.FloatField(verbose_name='平均评分')
    actors = models.TextField(blank=True, null=True, verbose_name='演员')
    storyline = models.TextField(blank=True, null=True,verbose_name='简介')
    vote = models.BigIntegerField(blank=True, null=True,verbose_name='评分数')
    feature=models.TextField(blank=True, null=True,verbose_name='特征')
    localimg = models.TextField(blank=True, null=True,verbose_name='图片')
    all_score=models.BigIntegerField(blank=True,null=True,verbose_name='总得分')
    # genreids = models.ManyToManyField(to=Genre, related_name="genre_movie", null=True, blank=True, default=None,verbose_name='类型id')
    # persons = models.ManyToManyField(to=Person, related_name="person_movie", null=True, blank=True, default=None,verbose_name='演员')
    imgfile = models.ImageField(blank=True, null=True, upload_to='moviecover/')


    def image_img(self):
        # 这里添加一个防空判断
        if not self.localimg:
            return '无'
        return format_html("""<div οnclick='$(".my_set_image_img").hide();$(this).next().show();'><img src='{}' style='width:50px;height:50px;' ></div><div class='my_set_image_img' οnclick="$('.my_set_image_img').hide()" style="z-index:9999;position:fixed; left: 100px; top:100px;display:none;"><img src='{}' style='width:500px; height:500px;'></div>""",self.localimg, self.localimg)

    image_img.short_description = '图片'

    class Meta:
        managed = True
        db_table = 'movie'
        verbose_name = '电影'  # 后台显示的表名
        verbose_name_plural = '电影管理'


class Rating(models.Model):
    ratingid = models.BigIntegerField(primary_key=True)
    movieid = models.BigIntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratingtime = models.CharField(max_length=255, blank=True, null=True)
    userid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rating'

class StayRating(models.Model):
    ratingid = models.BigIntegerField(primary_key=True)
    movieid = models.BigIntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratingtime = models.CharField(max_length=255, blank=True, null=True)
    userid = models.BigIntegerField(blank=True, null=True)
    favoriteid=models.BigIntegerField(default=0)
    class Meta:
        managed = True
        db_table = 'stayrating'

class Favorite(models.Model):
    favoriteid=models.BigIntegerField(primary_key=True)
    userid=models.BigIntegerField(blank=True, null=True)
    favoritename=models.CharField(max_length=255, blank=True, null=True, verbose_name='收藏夹名字')

    class Meta:
        managed = True
        db_table = 'favorite'

class CollectMovie(models.Model):
    id=models.BigIntegerField(primary_key=True)
    movieid = models.BigIntegerField(blank=True, null=True)
    favoriteid = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'collectmovie'


class User(models.Model):
    userid = models.BigIntegerField(primary_key=True,verbose_name='用户id')
    img = models.TextField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True,verbose_name='用户昵称')
    password = models.CharField(max_length=255, blank=True, null=True,verbose_name='用户密码')
    username = models.CharField(max_length=255, blank=True, null=True,verbose_name='用户名')
    watchitems=models.TextField(blank=True, default='')
    preference=models.TextField( blank=True, null=True)
    local=models.CharField(max_length=255,blank=True,null=True,verbose_name='用户所在地')
    selfnote=models.TextField(blank=True,null=True,verbose_name='个性签名')
    class Meta:
        managed = True
        db_table = 'user'
        verbose_name = '用户'  # 后台显示的表名
        verbose_name_plural = '用户管理'

class ItemSimilarity(models.Model):
    movieid = models.BigIntegerField(primary_key=True)
    itemsim=models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'itemsimilarity'

class UserPreference(models.Model):
    userid = models.BigIntegerField(primary_key=True)
    userpre=models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userpreference'

class ChatRecord(models.Model):
    chatid=models.BigIntegerField(primary_key=True)
    uid=models.BigIntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户昵称')
    content = models.TextField(blank=True, null=True)
    img=models.TextField(blank=True, null=True)
    type=models.BigIntegerField(blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'chatrecord'
