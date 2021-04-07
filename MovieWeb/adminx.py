import xadmin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import connection
from xadmin import views
from .models import *
# Register your models here.
class UserLargeTablePaginator(Paginator):
    def _get_count(self):
        return int(cache.get('userslen'))
    count = property(_get_count)

class CommentLargeTablePaginator(Paginator):
    def _get_count(self):
        return int(cache.get('commentslen'))
    count = property(_get_count)


class BaseSetting(object):
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "电影推荐网站后台管理系统"  # 设置站点标题
    site_footer = "电影推荐系统"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠，在左侧，默认的

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
    list_display = ['userid','nickname','username','password','local','selfnote']
    search_fields = ['userid','nickname','username','password','local','selfnote']
    list_editable = ['nickname','password','local','selfnote']
    list_display_links = ('userid','nickname','username','password','local','selfnote',)
    ordering = ('userid','nickname','username','password','local','selfnote',)
    readonly_fields = ('userid','username','watchitems','preference',)
    list_per_page = 20
    paginator_class=UserLargeTablePaginator

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
        cache.set('commenthistory' + str(user.userid), comments)  # 重新设置缓存
        res = {}
        res['data'] = comments
        cache.set('commentslen', int(cache.get('commentslen')) - 1)
    def has_add_permission(self, request=None):
        return False

    class Meta:
        verbose_name = '评论'

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Genre,GenreAdmin)
xadmin.site.register(User,UserAdmin)
xadmin.site.register(Comment,CommentAdmin)
