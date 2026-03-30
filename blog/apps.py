"""应用程序配置"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """应用配置类"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
