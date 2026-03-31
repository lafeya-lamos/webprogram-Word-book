"""主页视图"""

from django.shortcuts import render
from django.utils import timezone

from blog.models import Article


def format_russian_datetime(dt):
    """俄语日期显示"""
    weekdays = {
        0: 'понедельник',
        1: 'вторник',
        2: 'среда',
        3: 'четверг',
        4: 'пятница',
        5: 'суббота',
        6: 'воскресенье',
    }

    months = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря',
    }

    return (
        f"{weekdays[dt.weekday()]}, {dt.day} {months[dt.month]} {dt.year} г., "
        f"{dt.strftime('%H:%M')}"
    )


def _pluralize_ru(number, forms):
    """俄语复数"""
    if number == 1:
        return forms[0]
    if 2 <= number <= 4:
        return forms[1]
    return forms[2]

def format_time_ago_ru(dt):
    """俄语多久前显示"""
    now = timezone.localtime()
    dt = timezone.localtime(dt)
    delta = now - dt
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return "только что"

    minutes = seconds // 60
    if minutes < 60:
        suffix = _pluralize_ru(minutes, ("минуту", "минуты", "минут"))
        return f"{minutes} {suffix} назад"

    hours = minutes // 60
    if hours < 24:
        suffix = _pluralize_ru(hours, ("час", "часа", "часов"))
        return f"{hours} {suffix} назад"

    days = hours // 24
    suffix = _pluralize_ru(days, ("день", "дня", "дней"))
    return f"{days} {suffix} назад"

def index(request):
    """主页显示"""
    now = timezone.localtime()
    latest_article = Article.objects.order_by('-pub_date').first()

    if latest_article:
        last_added_text = format_time_ago_ru(latest_article.pub_date)
    else:
        last_added_text = "слов пока нет"

    context = {
        'welcome_title': 'Добро пожаловать!',
        'current_datetime': format_russian_datetime(now),
        'last_added_text': last_added_text,
    }
    return render(request, 'index.html', context)
