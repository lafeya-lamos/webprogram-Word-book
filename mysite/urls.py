from django.contrib import admin
from django.urls import path
from blog import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', views.article_list, name='article_list'),
    path('articles/add/', views.add_article, name='add_article'),
    path('articles/delete/<int:article_id>/', views.delete_article, name='delete_article'),
]
