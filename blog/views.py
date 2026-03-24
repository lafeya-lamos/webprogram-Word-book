from django.shortcuts import render, redirect, get_object_or_404 
from .forms import ArticleForm
from .models import Article

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('article_list')
    else:
        form = ArticleForm()
    articles = Article.objects.all().order_by('-pub_date')
    return render(request, 'blog/add_article.html', {'form': form, 'articles': articles})

def article_list(request):
    articles = Article.objects.all().order_by('-pub_date')  # 查询所有文章
    context = {
        'articles': articles
    }
    return render(request, 'blog/article_list.html', context)

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':          # 只允许 POST 删除
        article.delete()
        return redirect('article_list')   # 删除后跳转到列表页
    # 如果不是 POST，重定向到文章列表
    return redirect('article_list')
# Create your views here.

