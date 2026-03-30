# blog/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'title': 'Слово',
            'content': 'Значение',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Введите слово'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Введите перевод или объяснение слова'
            }),
        }
        error_messages = {
            'title': {
                'required': 'Пожалуйста, введите слово.',
                'max_length': 'Слово не должно превышать 200 символов.',
            },
            'content': {
                'required': 'Пожалуйста, введите значение слова.',
            },
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        existing = Article.objects.filter(title__iexact=title)

        # 编辑时排除自己
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError("Это слово уже есть в словаре.")

        return title

    def clean_content(self):
        content = self.cleaned_data['content'].strip()

        if not content:
            raise forms.ValidationError("Пожалуйста, введите значение слова.")

        return content
