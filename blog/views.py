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

def generate_quiz_questions(num_questions=5):
    # 按录入顺序排序（最早录入在前）
    all_words = list(Article.objects.all().order_by('pub_date', 'id'))

    if len(all_words) < num_questions:
        return None, f"词库数量不足，至少需要 {num_questions} 个单词才能生成测试。当前只有 {len(all_words)} 个。"

    # 从全部单词中随机抽 num_questions 个作为题目
    selected_words = random.sample(all_words, num_questions)

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

        # 如果 ±2 范围内刚好没有可用错误项（极端兜底）
        if neighbor_candidates:
            nearby_wrong = random.choice(neighbor_candidates)
        else:
            # 兜底：从其他单词中补一个
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
    if request.method == 'POST':
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
            'total': total,
        })

    # GET 请求
    num_questions_str = request.GET.get('num_questions')

    # 首次进入页面，没有 num_questions 参数，只显示数量选择表单，不生成题目
    if num_questions_str is None:
        return render(request, 'blog/quiz.html', {
            'submitted': False,
            'questions': None,   # 没有题目
            'num_questions': 5,  # 默认值用于表单显示
        })

    # 有 num_questions 参数，进行验证
    input_error = None
    num_questions = None
    questions = None

    try:
        num_questions = int(num_questions_str)
        if num_questions < 1 or num_questions > 20:
            input_error = "题目数量必须是 1 到 20 之间的整数。"
        else:
            questions, error = generate_quiz_questions(num_questions)
            if error:
                input_error = error
                questions = None
    except ValueError:
        input_error = "题目数量必须是数字。"

    return render(request, 'blog/quiz.html', {
        'submitted': False,
        'questions': questions,
        'error': input_error,
        'num_questions': num_questions if num_questions is not None else 5,
    })

# Create your views here.

