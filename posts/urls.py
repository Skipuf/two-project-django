from django.urls import path

from posts.views import (PostList, PostDetail, PostSearch,
                         CreateNews, EditPost, DelPost,
                         CreateArticles)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search', PostSearch.as_view(), name='post_search'),
    path('create/news', CreateNews.as_view(), name='create_news'),
    path('<int:pk>/edit', EditPost.as_view(), name='edit_post'),
    path('<int:pk>/del', DelPost.as_view(), name="del_post"),
    path('create/articles', CreateArticles.as_view(), name='create_articles'),
]