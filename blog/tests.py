"""测试模块"""

from django.test import TestCase

from .models import Article


class ArticleModelTest(TestCase):
    """Article模型简单测试"""

    def test_article_creation(self):
        """创建测试"""
        article = Article.objects.create(
            title='Тестовое слово',
            content='Тестовое значение'
        )
        self.assertEqual(article.title, 'Тестовое слово')
        self.assertEqual(str(article), 'Тестовое слово')
