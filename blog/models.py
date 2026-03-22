from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='单词')      # 添加 verbose_name
    content = models.TextField(verbose_name='释义')                    # 添加 verbose_name
    pub_date = models.DateTimeField(auto_now_add=True)  # 发布时间

    def __str__(self):
        return self.title
# Create your models here.
