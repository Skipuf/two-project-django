from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_post = 0
        for item in Post.objects.filter(author=self).values('rating'):
            rating_post += item['rating']
        rating_com = 0
        for item in Comment.objects.filter(author=self.user_id).values('rating'):
            rating_com += item['rating']
        rating_com_posts = 0
        for item in Comment.objects.filter(post__author=self).values('rating'):
            rating_com_posts += item['rating']
        self.rating = (rating_post * 3) + rating_com + rating_com_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'ar'
    news = 'ne'

    POSITIONS = [
        (article, 'статья'),
        (news, 'новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2,
                                 choices=POSITIONS,
                                 default='ar')
    datetime_creation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        return self.content[:124] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    datetime_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()
