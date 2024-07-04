from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import FormCreateNews, FormEditPost
from .models import Post
from .filters import NewsFilter


class PostSearch(ListView):
    model = Post
    ordering = '-datetime_creation'
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-datetime_creation'
    template_name = 'posts.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'new'


# Добавляем новое представление для создания товаров.
class CreateNews(CreateView):
    # Указываем нашу разработанную форму
    form_class = FormCreateNews
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = Post.news
        return super().form_valid(form)


class CreateArticles(CreateView):
    form_class = FormCreateNews
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = Post.article
        return super().form_valid(form)


class EditPost(UpdateView):
    form_class = FormEditPost
    model = Post
    template_name = 'post_edit.html'


class DelPost(DeleteView):
    model = Post
    template_name = 'post_del.html'
    success_url = reverse_lazy('post_list')
