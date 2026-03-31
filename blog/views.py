"""视图模块"""

import random

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import ArticleForm
from .models import Article, WrongWordRecord


def add_article(request):
    """添加新单词"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()  # 直接保存到数据库
            messages.success(request, "Слово успешно добавлено!")
            return redirect('add_article')  # 重定向到添加单词页
    else:
        form = ArticleForm()

    # 取最近答错记录（按时间倒序）
    recent_wrong_records = WrongWordRecord.objects.select_related('word').order_by('-wrong_time')

    # 去重后取最近 5 个单词
    recent_wrong_words = []
    seen_word_ids = set()

    for record in recent_wrong_records:
        if record.word.id not in seen_word_ids:
            recent_wrong_words.append(record.word)
            seen_word_ids.add(record.word.id)

        if len(recent_wrong_words) >= 5:
            break

    return render(request, 'blog/add_article.html', {
        'form': form,
        'recent_wrong_words': recent_wrong_words
    })

def article_list(request):
    """单词列表显示和按单词或释义搜索"""
    query = request.GET.get('q', '').strip()
    articles = Article.objects.all().order_by('-pub_date')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    context = {
        'articles': articles,
        'query': query,
    }
    return render(request, 'blog/article_list.html', context)

def delete_article(request, article_id):
    """删除单词"""
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':          # 只允许 POST 删除
        article.delete()
        return redirect('article_list')   # 删除后跳转到列表页
    # 如果不是 POST，重定向到文章列表
    return redirect('article_list')

def edit_article(request, article_id):
    """编辑单词"""
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/edit_article.html', {
        'form': form,
        'article': article,
    })

def _get_neighbor_wrong(word, all_words, current_index):
    """获取邻近位置（±2）的错误选项，若无则兜底从其他单词中选一个。"""
    candidates = [
        all_words[j]
        for j in range(max(0, current_index - 2), min(len(all_words), current_index + 3))
        if j != current_index and all_words[j].content != word.content
    ]
    if candidates:
        return random.choice(candidates)
    # 兜底：任意一个不同的错误选项
    fallback = [w for w in all_words if w.id != word.id and w.content != word.content]
    if not fallback:
        raise ValueError("Недостаточно слов для создания варианта ошибки.")
    return random.choice(fallback)


def _get_random_wrong(word, exclude_word, all_words):
    """获取一个随机错误选项，排除当前单词和 exclude_word"""
    candidates = [
        w for w in all_words
        if w.id != word.id and w.id != exclude_word.id and w.content != word.content
    ]
    if candidates:
        return random.choice(candidates)
    # 兜底：任意一个不同的错误选项（仅排除当前词）
    backup = [w for w in all_words if w.id != word.id and w.content != word.content]
    if not backup:
        raise ValueError("Недостаточно слов для создания варианта ошибки.")
    return random.choice(backup)

def _build_options(word, correct_meaning, nearby_wrong, random_wrong, all_words):
    """构建选项列表，去重并确保至少 3 个不同选项"""
    options = [
        {"text": correct_meaning, "is_correct": True},
        {"text": nearby_wrong.content, "is_correct": False},
        {"text": random_wrong.content, "is_correct": False},
    ]

    # 去重（基于文本）
    unique_texts = set()
    deduped = []
    for opt in options:
        if opt["text"] not in unique_texts:
            deduped.append(opt)
            unique_texts.add(opt["text"])

    # 如果不足 3 个选项，补充额外的随机错误项
    if len(deduped) < 3:
        extra_candidates = [
            w for w in all_words
            if w.id != word.id and w.content not in unique_texts
        ]
        while len(deduped) < 3 and extra_candidates:
            extra = random.choice(extra_candidates)
            deduped.append({"text": extra.content, "is_correct": False})
            unique_texts.add(extra.content)
            extra_candidates = [
                w for w in all_words
                if w.id != word.id and w.content not in unique_texts
            ]
    # 如果补充后仍然不足3个，说明题库太小，抛出错误
    if len(deduped) < 3:
        raise ValueError(f"Недостаточно уникальных вариантов ответа для слова '{word.title}'.")

    random.shuffle(deduped)
    return deduped

def generate_quiz_questions(num_questions=5, mode='random'):
    """生成测试题"""
    all_words = list(Article.objects.all().order_by('pub_date', 'id'))

    if len(all_words) < 5:
        return None, (
            f"Количество слов слишком мало(только {len(all_words)}), "
            f"генерация задания, скорее всего, не удастся, добавьте больше слов!."
        )
    if len(all_words) < num_questions:
        return None, (
            f"Недостаточно слов в словаре. Для теста нужно минимум "
            f"{num_questions} слов, сейчас доступно только {len(all_words)}."
        )

    # 根据模式选择单词
    if mode == 'random':
        selected_words = random.sample(all_words, num_questions)
    elif mode == 'review':
        selected_words = all_words[-num_questions:]
    else:
        selected_words = random.sample(all_words, num_questions)

    questions = []
    for idx, word in enumerate(selected_words, start=1):
        try:
            current_index = all_words.index(word)
            correct_meaning = word.content

            nearby_wrong = _get_neighbor_wrong(word, all_words, current_index)
            random_wrong = _get_random_wrong(word, nearby_wrong, all_words)
            options = _build_options(word, correct_meaning, nearby_wrong, random_wrong, all_words)
        except ValueError as e:
            # 捕获底层抛出的错误
            return None, str(e)

        questions.append({
            "question_no": idx,
            "word": word.title,
            "options": options,
            "correct_answer": correct_meaning,
        })

    return questions, None

def _process_quiz_submission(request):
    """处理测试POST请求，返回HTTP响应"""
    total = request.POST.get('total_questions')
    try:
        total = int(total)
        if total < 1 or total > 20:
            return redirect('quiz')
    except (TypeError, ValueError):
        return redirect('quiz')

    questions = []
    score = 0

    for i in range(1, total + 1):
        word = request.POST.get(f'word_{i}')
        correct_answer = request.POST.get(f'correct_{i}')
        selected_answer = request.POST.get(f'question_{i}')

        is_correct = (selected_answer == correct_answer) if selected_answer else False
        if is_correct:
            score += 1
        else:
            wrong_article = Article.objects.filter(title=word).first()
            if wrong_article:
                WrongWordRecord.objects.create(word=wrong_article)

        questions.append({
            "question_no": i,
            "word": word,
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "answered": selected_answer is not None
        })

    return render(
        request,
        'blog/quiz.html',
        {
            'submitted': True,
            'questions': questions,
            'score': score,
            'total': total,
        }
    )


def _prepare_quiz_questions(num_questions, mode):
    """测试题数量限制及报错"""
    try:
        num_questions = int(num_questions)
        if num_questions < 1 or num_questions > 20:
            return None, "Количество вопросов должно быть целым числом от 1 до 20.", num_questions
        questions, error = generate_quiz_questions(num_questions, mode)
        if error:
            return None, error, num_questions
        return questions, None, num_questions
    except ValueError:
        return None, "Количество вопросов должно быть целым числом.", None


def quiz_view(request):
    """按输入数量及模式生成测试"""
    if request.method == 'POST':
        return _process_quiz_submission(request)

    # GET请求
    num_questions_str = request.GET.get('num_questions')
    mode = request.GET.get('mode', 'random')

    # 初次进入页面
    if num_questions_str is None:
        return render(
            request,
            'blog/quiz.html',
            {
                'submitted': False,
                'questions': None,
                'num_questions': 5,
                'mode': mode,
            }
        )

    # 按要求生成测试
    questions, error, validated_num = _prepare_quiz_questions(num_questions_str, mode)
    return render(
        request,
        'blog/quiz.html',
        {
            'submitted': False,
            'questions': questions,
            'error': error,
            'num_questions': validated_num if validated_num is not None else 5,
            'mode': mode,
        }
    )



