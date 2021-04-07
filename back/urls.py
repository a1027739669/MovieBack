"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import MovieWeb.views as views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from . import settings
import xadmin
from xadmin.plugins import xversion
xversion.register_models()
xadmin.autodiscover()



urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', views.set_watch),
    path('user/login/', views.user_login),
    path('movies/highscoremovie/',views.get_high_score_movies),
    path('movie/',views.get_movie_by_id),
    path('person/',views.get_person_by_id),
    path('movie/douban/',views.get_movie_name_and_img_by_id),
    path('movies/unlogintoday/',views.get_recom_movies_unlogin),
    path('searches/movies/',views.searches_movies),
    path('accounts/password',views.update_password),
    path('movies/today/',views.get_recom_movies),
    path('movies/rating/',views.submit_rating),
    path('movies/comment/',views.submit_comment),
    path('movies/ratinglist/',views.get_rating_list),
    path('movies/commentlist/',views.get_comment_list),
    path('movies/deletecomment/',views.delete_comment),
    path('email',views.send_email),
    path('authentication/account',views.register),
    path('movies/search',views.searches_movie_by_keyword),
    path('persons/search',views.searches_person_by_keyword),
    path('movies/alsolike',views.get_also_like),
    path('user/upload',views.upload_user_img),
    path('user/save',views.sava_user_img_to_db),
    path('user/update/',views.update_user_profile),
    path('persons/today',views.get_persons),
    path('message/save/',views.save_message),
    path('message/get',views.get_meaaage),
    path('movies/curmovies',views.get_cur_movies),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

