# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    commentid = models.BigIntegerField(primary_key=True,verbose_name='id')
    commenttime = models.CharField(max_length=255, blank=True, null=True,verbose_name='评论时间')
    content = models.TextField(blank=True, null=True,verbose_name='评论内容')
    movieid = models.BigIntegerField(blank=True, null=True,verbose_name='电影id')
    userid = models.BigIntegerField(blank=True, null=True,verbose_name='用户id')
    class Meta:
        managed = True
        db_table = 'comment'
        verbose_name = '评论'  # 后台显示的表名
        verbose_name_plural = '评论管理'


class Genre(models.Model):
    id = models.BigIntegerField(primary_key=True)
    genrename = models.CharField(max_length=255, blank=True, null=True,verbose_name='类型名')

    class Meta:
        managed = True
        db_table = 'genre'
        verbose_name = '类型'  # 后台显示的表名
        verbose_name_plural = '类型管理'  # 后台显示的表名复数 英语复数是加s 这里我们写死为 要显示的表名


class Movie(models.Model):
    movieid = models.BigIntegerField(primary_key=True)
    actorid = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    cover = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    directorid = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    minus = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    relesetime = models.CharField(max_length=255, blank=True, null=True)
    year= models.CharField(max_length=255, blank=True, null=True)
    score = models.FloatField()
    storyline = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    vote = models.BigIntegerField(blank=True, null=True)
    feature=models.TextField(blank=True, null=True)
    localimg = models.TextField(blank=True, null=True)
    all_score=models.BigIntegerField(blank=True,null=True)
    genreids = models.ManyToManyField(to=Genre, related_name="genre_movie", null=True, blank=True, default=None)
    class Meta:
        managed = True
        db_table = 'movie'


class Person(models.Model):
    personid = models.BigIntegerField(primary_key=True)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    birthplace = models.CharField(max_length=255, blank=True, null=True)
    blog = models.TextField(blank=True, null=True)
    constellation = models.CharField(max_length=255, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    nameen = models.TextField(blank=True, null=True)
    namezh = models.TextField(blank=True, null=True)
    profession = models.TextField(blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    img=models.TextField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'person'


class Rating(models.Model):
    ratingid = models.BigIntegerField(primary_key=True)
    movieid = models.BigIntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratingtime = models.CharField(max_length=255, blank=True, null=True)
    userid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rating'


class User(models.Model):
    userid = models.BigIntegerField(primary_key=True,verbose_name='用户id')
    img = models.TextField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True,verbose_name='用户昵称')
    password = models.CharField(max_length=255, blank=True, null=True,verbose_name='用户密码')
    username = models.CharField(max_length=255, blank=True, null=True,verbose_name='用户名')
    watchitems=models.TextField(blank=True, null=True)
    preference=models.TextField( blank=True, null=True)
    local=models.CharField(max_length=255,blank=True,null=True)
    selfnote=models.TextField(blank=True,null=True)
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
    msg = models.TextField(blank=True, null=True)
    img=models.TextField(blank=True, null=True)
    type=models.BigIntegerField(blank=True, null=True)
    chattime = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'chatrecord'