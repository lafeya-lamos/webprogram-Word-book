from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)      # 标题
    content = models.TextField()                   # 内容
    pub_date = models.DateTimeField(auto_now_add=True)  # 发布时间

    def __str__(self):
        return self.title
# Create your models here.
