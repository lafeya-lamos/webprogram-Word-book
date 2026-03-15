from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()  # 直接保存到数据库
            return redirect('article_list')  # 重定向到文章列表页
    else:
        form = ArticleForm()
    return render(request, 'blog/add_article.html', {'form': form})

def article_list(request):
    """从数据库获取所有文章，按发布时间倒序排列，然后渲染到模板"""
    articles = Article.objects.all().order_by('-pub_date')  # 查询所有文章
    context = {
        'articles': articles
    }
    return render(request, 'blog/article_list.html', context)
# Create your views here.
