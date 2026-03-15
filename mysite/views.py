from django.shortcuts import render

def index(request):
    """简单的首页视图，渲染 index.html 模板"""
    context = {
        'message': '欢迎访问我的 Django 项目！'
    }
    return render(request, 'index.html', context)