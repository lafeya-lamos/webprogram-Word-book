from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Слово') 
    content = models.TextField(verbose_name='Значение')                    
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class WrongWordRecord(models.Model):
    word = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='wrong_records')
    wrong_time = models.DateTimeField(auto_now_add=True, verbose_name='答错时间')

    def __str__(self):
        return f"{self.word.title} - {self.wrong_time}"

# Create your models here.
