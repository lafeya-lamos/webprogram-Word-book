from django.shortcuts import render
from django.utils import timezone
from blog.models import Article


def format_russian_datetime(dt):
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

    return f"{weekdays[dt.weekday()]}, {dt.day} {months[dt.month]} {dt.year} г., {dt.strftime('%H:%M')}"


def format_time_ago_ru(dt):
    now = timezone.localtime()
    dt = timezone.localtime(dt)
    delta = now - dt

    seconds = int(delta.total_seconds())

    if seconds < 60:
        return "только что"

    minutes = seconds // 60
    if minutes < 60:
        if minutes == 1:
            return "1 минуту назад"
        elif 2 <= minutes <= 4:
            return f"{minutes} минуты назад"
        else:
            return f"{minutes} минут назад"

    hours = minutes // 60
    if hours < 24:
        if hours == 1:
            return "1 час назад"
        elif 2 <= hours <= 4:
            return f"{hours} часа назад"
        else:
            return f"{hours} часов назад"

    days = hours // 24
    if days == 1:
        return "1 день назад"
    elif 2 <= days <= 4:
        return f"{days} дня назад"
    else:
        return f"{days} дней назад"


def index(request):
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
