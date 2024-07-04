from django import forms

from .models import Post


class FormCreateNews(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author',
            'categories',
        ]
        labels = {
            'author': 'Автор',
            'title': 'Название',
            'categories': 'Категории',
            'content': 'Содержание',
        }


class FormEditPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'categories'
        ]
        labels = {
            'title': 'Название',
            'categories': 'Категории',
            'content': 'Содержание',
        }
