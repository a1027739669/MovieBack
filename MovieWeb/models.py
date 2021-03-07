# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    commentid = models.BigIntegerField(primary_key=True)
    commenttime = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    movieid = models.BigIntegerField(blank=True, null=True)
    rating = models.BigIntegerField(blank=True, null=True)
    userid = models.BigIntegerField(blank=True, null=True)
    vote = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comment'


class Genre(models.Model):
    id = models.BigIntegerField(primary_key=True)
    genrename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'genre'


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
    score = models.FloatField()
    storyline = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    vote = models.BigIntegerField(blank=True, null=True)

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
    userid = models.BigIntegerField(primary_key=True)
    img = models.TextField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    watchitems=models.TextField(blank=True, null=True)
    preference=models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'user'
