from django.views.generic import ListView, DetailView

from .models import Post


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = '-datetime_creation'
    template_name = 'news.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'