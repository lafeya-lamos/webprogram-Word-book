from django.shortcuts import render, redirect, get_object_or_404 
from .forms import ArticleForm
from .models import Article
import random

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

def generate_quiz_questions():
    # 按录入顺序排序（最早录入在前）
    all_words = list(Article.objects.all().order_by('pub_date', 'id'))

    # 单词不足报错
    if len(all_words) < 5:
        return None, "词库数量不足，至少需要 5 个单词才能生成测试。"

    # 从全部单词中随机抽 5 个作为题目
    selected_words = random.sample(all_words, 5)

    questions = []

    for q_index, word in enumerate(selected_words, start=1):
        current_index = all_words.index(word)
        correct_meaning = word.content

        # 1) 邻近错误选项（±2）
        neighbor_candidates = [
            all_words[j]
            for j in range(max(0, current_index - 2), min(len(all_words), current_index + 3))
            if j != current_index and all_words[j].content != correct_meaning
        ]

        # 如果 ±2 范围内刚好没有可用错误项（极端）
        if neighbor_candidates:
            nearby_wrong = random.choice(neighbor_candidates)
        else:
            # 从其他单词中补一个
            fallback_candidates = [
                w for w in all_words
                if w.id != word.id and w.content != correct_meaning
            ]
            nearby_wrong = random.choice(fallback_candidates)

        # 2) 其他随机错误选项
        random_wrong_candidates = [
            w for w in all_words
            if w.id != word.id
            and w.id != nearby_wrong.id
            and w.content != correct_meaning
        ]

        # 极端
        if random_wrong_candidates:
            random_wrong = random.choice(random_wrong_candidates)
        else:
            backup_candidates = [
                w for w in all_words
                if w.id != word.id and w.content != correct_meaning
            ]
            random_wrong = random.choice(backup_candidates)

        options = [
            {"text": correct_meaning, "is_correct": True},
            {"text": nearby_wrong.content, "is_correct": False},
            {"text": random_wrong.content, "is_correct": False},
        ]

        # 防止极端情况下两个错误选项文字重复（比如释义内容完全一样）
        unique_texts = set()
        deduped_options = []
        for opt in options:
            if opt["text"] not in unique_texts:
                deduped_options.append(opt)
                unique_texts.add(opt["text"])

        # 如果去重后不足 3 个选项，则继续补随机错误项
        if len(deduped_options) < 3:
            extra_candidates = [
                w for w in all_words
                if w.id != word.id and w.content not in unique_texts
            ]
            while len(deduped_options) < 3 and extra_candidates:
                extra = random.choice(extra_candidates)
                deduped_options.append({"text": extra.content, "is_correct": False})
                unique_texts.add(extra.content)
                extra_candidates = [
                    w for w in all_words
                    if w.id != word.id and w.content not in unique_texts
                ]

        random.shuffle(deduped_options)

        questions.append({
            "question_no": q_index,
            "word": word.title,
            "options": deduped_options,
            "correct_answer": correct_meaning,
        })

    return questions, None


def quiz_view(request):
    """
    测试页面：
    - GET：生成 5 道题
    - POST：提交答案并显示结果
    """
    if request.method == 'POST':
        questions = []
        score = 0

        for i in range(1, 6):
            word = request.POST.get(f'word_{i}')
            correct_answer = request.POST.get(f'correct_{i}')
            selected_answer = request.POST.get(f'question_{i}')

            is_correct = selected_answer == correct_answer
            if is_correct:
                score += 1

            questions.append({
                "question_no": i,
                "word": word,
                "selected_answer": selected_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "answered": selected_answer is not None
            })

        return render(request, 'blog/quiz.html', {
            'submitted': True,
            'questions': questions,
            'score': score,
            'total': 5,
        })

    # GET 请求：生成新题目
    questions, error = generate_quiz_questions()

    return render(request, 'blog/quiz.html', {
        'submitted': False,
        'questions': questions,
        'error': error,
    })

# Create your views here.

