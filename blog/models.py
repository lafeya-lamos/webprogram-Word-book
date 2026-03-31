"""存储单词和错误记录的模型"""

from django.db import models

class Article(models.Model):
    """单词及释义模型"""

    title = models.CharField(max_length=200, verbose_name='Слово')
    content = models.TextField(verbose_name='Значение')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self) -> str:
        return str(self.title)

class WrongWordRecord(models.Model):
    """错误记录模型"""
    word = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='wrong_records')
    wrong_time = models.DateTimeField(auto_now_add=True, verbose_name='wrong time')

    def __str__(self) -> str:
        return f"{self.word.title} - {self.wrong_time}"
