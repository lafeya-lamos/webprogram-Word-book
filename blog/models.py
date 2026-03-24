from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Слово') 
    content = models.TextField(verbose_name='Значение')                    
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Create your models here.
