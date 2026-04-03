# Vocabulary Trainer / Тренажёр слов

## 项目简介 / Описание проекта

- 这是一个使用 Django 开发的词汇学习网站，用户可以添加、编辑、删除单词，并通过测试功能进行记忆训练。  
- Это веб-приложение для изучения слов, созданное с помощью Django. Пользователь может добавлять, редактировать и удалять слова, а также проходить тесты для запоминания.

---

## 主要功能 / Основные функции

- 添加单词 / Добавление слов
- 编辑单词 / Редактирование слов
- 删除单词 / Удаление слов
- 单词列表 / Список слов
- 搜索功能 / Поиск слов
- 测试功能 / Тестирование
- 错题记录 / Учёт ошибок

---

## 技术栈 / Технологии

- Python
- Django
- SQLite
- HTML
- CSS

---

## 项目结构 / Структура проекта

- ├── blog/                  # 主应用
- │   ├── migrations/        # 数据库迁移文件
- │   ├── templates/         # HTML 模板
- │   ├── static/            # CSS / 静态资源
- │   ├── admin.py
- │   ├── forms.py
- │   ├── models.py
- │   ├── tests.py
- │   ├── urls.py
- │   └── views.py
- │
- ├── mysite/                # Django 项目配置
- │   ├── settings.py
- │   ├── urls.py
- │   ├── tests.py
- │   └── wsgi.py
- ├── db.sqlite3             # SQLite 数据库
- ├── manage.py
- ├── requirements.txt
- └── README.md

---

## 本地运行 / Локальный запуск

### 1.创建虚拟环境并激活(非必要) / Создать и активировать виртуальное окружение(необязательно)

python -m venv venv

- Windows:
venv\Scripts\activate

- macOS / Linux:
source venv/bin/activate

### 2.安装依赖 / Установить зависимости

pip  install -r requirements.txt

### 3.数据库迁移 / Миграции базы данных

python manage.py makemigrations blog
python manage.py migrate

### 4.启动项目 / Запустить проект

python manage.py runserver

- 打开浏览器 / Откройте в браузере:

http://127.0.0.1:8000/

---

## 碎碎念

- 祈祷🙏
终末地1.2不出庄方宜🙏。。终末地1.2不出庄方宜🙏。。终末地1.2不出庄方宜🙏。。
