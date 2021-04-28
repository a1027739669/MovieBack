import xadmin
from django.core.cache import cache
from django.core.paginator import Paginator
from xadmin import views
from .models import *
# Register your models here.
from program.cbrec import *
cbrec = CBRec()
class UserLargeTablePaginator(Paginator):
    def _get_count(self):
        return int(cache.get('userslen'))
    count = property(_get_count)

class CommentLargeTablePaginator(Paginator):
    def _get_count(self):
        return int(cache.get('commentslen'))
    count = property(_get_count)

class PersonLargeTablePaginator(Paginator):
    def _get_count(self):
        return int(cache.get('personslen'))
    count = property(_get_count)

class MovieLargeTablePaginator(Paginator):
    def _get_count(self):
        return int(cache.get('movieslen'))
    count = property(_get_count)



class BaseSetting(object):
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "电影推荐网站后台管理系统"  # 设置站点标题
    site_footer = "电影推荐系统"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠，在左侧，默认的

class MovieAdmin(object):
    list_display = ['movieid','name','alias','actors','director', 'genre', 'language', 'region', 'relesetime','score','image_img']
    search_fields = ['movieid','name','alias','actors','director', 'genre', 'language', 'region', 'relesetime','storyline','score','image_img']
    list_editable = ['name','alias','persons','director', 'genre', 'language', 'region', 'relesetime','storyline','image_img']
    list_display_links = ('movieid','name','alias','actors','director', 'genre', 'language', 'region', 'relesetime','storyline','score','image_img',)
    ordering = ('movieid', 'relesetime','score',)
    readonly_fields = ('movieid','actorid','directorid','genre','year','score','vote','feature','localimg','all_score','actors',)
    filter_horizontal=('genreids','persons',)
    style_fields={'genreids':'m2m_transfer','persons':'m2m_transfer'}
    list_per_page = 20
    paginator_class = MovieLargeTablePaginator
    def save_models(self):  #重写保存电影方法
        obj=self.new_obj
        if obj.movieid == None:
            movieslen= int(cache.get('movieslen'))
            movieslen+=1
            cache.set('movieslen',movieslen,60*60*24*365)

        persons = list(obj.persons.all().values())
        li = []
        movie_actors = ''
        for person in persons[:-1]:
            li.extend([str(person['name']), '/'])
        li.extend([str(persons[-1]['name'])])
        movie_actors = movie_actors.join(li)
        obj.actors = movie_actors

        if(obj.actors!=None and obj.actorid!=None):
            actors=obj.actors.split('/')
            actorid=''
            li=[]
            for actor in actors[:-1]:
                li.extend([str(actor),':',str(Person.objects.filter(name=actor)[0].personid),'|'])
            li.extend([str(actors[-1]),':',str(Person.objects.filter(name=actors[-1])[0].personid)])
            actorid=actorid.join(li)
            obj.actorid =actorid

        try:
            url = 'http://127.0.0.1:8000/media/moviecover/' + obj.imgfile.url.split('/')[-1]
            obj.img = url
        except ValueError:
            pass
        genres=list(obj.genreids.all().values())
        li=[]
        movie_genre=''
        for genre in genres[:-1]:
            li.extend([str(genre['genrename']),'/'])
        li.extend([str(genres[-1]['genrename'])])
        movie_genre=movie_genre.join(li)
        obj.genre = movie_genre

        genres = Genre.objects.all()
        feature = ''
        movie_genres = obj.genre.split('/')
        for genre in genres:
            if genre.genrename in movie_genres:
                feature += str(genre.id) + ':' + str(1.0) + '/'
            else:
                feature += str(genre.id) + ':' + str(0) + '/'

        obj.feature = feature
        obj.save()
    def has_delete_permission(self, request=None):
        return False

class PersonAdmin(object):
    list_display = ['personid','name','nameen','namezh', 'birthday', 'birthplace', 'constellation', 'profession','sex','image_img']
    search_fields = ['personid', 'birthday', 'birthplace', 'blog', 'constellation', 'name','nameen','namezh','profession','sex']
    list_editable = [ 'birthday', 'birthplace', 'blog', 'constellation', 'name','nameen','namezh','profession','sex']
    list_display_links = ('personid', 'birthday', 'birthplace', 'blog', 'constellation', 'name','nameen','namezh','profession','sex','img',)
    ordering = ('personid', 'birthday', 'birthplace', 'constellation', 'name','nameen','namezh',)
    readonly_fields = ('personid','img',)
    list_per_page = 20
    paginator_class = PersonLargeTablePaginator
    def save_models(self):
        obj = self.new_obj
        if obj.personid == None:
            personslen= int(cache.get('personslen'))
            personslen+=1
            cache.set('personslen',personslen,60*60*24*365)
        if obj.imgfile!=None:
            url='http://127.0.0.1:8000/media/personimg/'+obj.imgfile.url.split('/')[-1]
            obj.img=url
        obj.save()
    def has_delete_permission(self, request=None):
        return False

class GenreAdmin(object):
    list_display = ['id','genrename']
    search_fields = ['id','genrename']
    list_display_links = ('id','genrename')
    ordering = ('id','genrename',)
    readonly_fields = ('id',)
    list_per_page = 20
    def save_models(self):
        obj=self.new_obj
        if obj.id !=None:
            genre=Genre.objects.get(id=obj.id)
            movies=Movie.objects.filter(genre__icontains=genre.genrename)
            for movie in movies:
                newgenre=str(movie.genre).replace(genre.genrename,obj.genrename)
                movie.genre=newgenre
                movie.save()
            obj.save()
        else:
            obj.save()

    def has_delete_permission(self, request=None):
        # Disable delete
        return False
    class Meta:
        verbose_name='标签'

class UserAdmin(object):
    list_display = ['userid','nickname','username','password','local']
    search_fields = ['userid','nickname','username','password','local','selfnote']
    list_editable = ['nickname','password','local','selfnote']
    list_display_links = ('userid','nickname','username','password','local','selfnote',)
    ordering = ('userid','nickname','username','password','local','selfnote',)
    readonly_fields = ('userid','username','watchitems','preference',)
    list_per_page = 20
    paginator_class=UserLargeTablePaginator
    def sava_models(self):
        obj=self.new_obj
        if obj.watchitems==None:
            obj.watchitems=''
        obj.save()
    def has_add_permission(self, request=None):
        return False
    class Meta:
        verbose_name='用户'


class CommentAdmin(object):
    list_display = ['commentid', 'commenttime', 'content', 'movieid', 'userid']
    search_fields = ['commentid', 'commenttime', 'content', 'movieid', 'userid']
    list_editable = [ 'content']
    list_display_links = ('commentid', 'commenttime', 'content', 'movieid', 'userid',)
    ordering = ('commentid', 'commenttime', 'content', 'movieid', 'userid',)
    readonly_fields = ('commentid', 'commenttime', 'movieid', 'userid',)
    list_per_page = 20
    paginator_class = CommentLargeTablePaginator

    def delete_model(self):
        comment=self.obj
        commentid=comment.commentid
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
        cache.set('commenthistory' + str(user.userid), comments,60*60*24)  # 重新设置缓存
        res = {}
        res['data'] = comments
        cache.set('commentslen', int(cache.get('commentslen')) - 1,60*60*24*365)
    def has_add_permission(self, request=None):
        return False

    class Meta:
        verbose_name = '评论'

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Movie,MovieAdmin)
xadmin.site.register(Person,PersonAdmin)
xadmin.site.register(Genre,GenreAdmin)
xadmin.site.register(User,UserAdmin)
xadmin.site.register(Comment,CommentAdmin)
