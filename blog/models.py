from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='单词') 
    content = models.TextField(verbose_name='释义')                    
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Create your models here.
