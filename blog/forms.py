"""表单模块"""

from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):
    """创建和修改单词及释义"""

    class Meta:
        """表单配置内部类"""
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
        """验证单词唯一性，删除俩端空格"""
        title = self.cleaned_data['title'].strip()

        existing = Article.objects.filter(title__iexact=title)

        # 编辑时排除自己
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError("Это слово уже есть в словаре.")

        return title

    def clean_content(self):
        """释义字段验证，删除两端空格及非空验证"""
        content = self.cleaned_data['content'].strip()

        if not content:
            raise forms.ValidationError("Пожалуйста, введите значение слова.")

        return content
