"""管理面板模块"""

from django.contrib import admin

from .models import Article, WrongWordRecord

admin.site.register(Article)
admin.site.register(WrongWordRecord)

# Register your models here.
