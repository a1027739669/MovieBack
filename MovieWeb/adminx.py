import xadmin
from django.core.paginator import Paginator
from django.db import connection
from xadmin import views
from .models import *
# Register your models here.
cursor=connection.cursor()

class BaseSetting(object):
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "电影推荐网站后台管理系统"  # 设置站点标题
    site_footer = "xxxxxxx"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠，在左侧，默认的

class GenreAdmin(object):
    list_display = ['id','genrename']
    search_fields = ['id','genrename']
    list_editable = ['genrename']
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



xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Genre,GenreAdmin)
