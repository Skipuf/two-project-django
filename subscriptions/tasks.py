from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from posts.models import Category, Post


@shared_task
def send_email_create_post(post):
    categories = Category.objects.filter(post__id=post).values("id", "name")
    post = Post.objects.get(id=post)
    emails_set = set()
    for category_id in categories:
        emails = User.objects.filter(
            subscriber__category=category_id['id']
        ).values_list('email', flat=True)
        emails_set.update(emails)
    if emails_set:
        title = post.title
        content = " ".join(post.content.split(" ")[:20:])
        subject = f'Новый пост в категориях: {", ".join([category_name["name"] for category_name in categories])}'
        text_content = (
            f'{title}\n'
            f'{content}\n\n'
            f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}'
        )
        html_content = (
            f'{title}<br>'
            f'{content}<br><br>'
            f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails_set:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def weekly_newsletter():
    emails_users = {}

    now = datetime.now(pytz.utc)
    seven_days_ago = now - timedelta(days=7)

    posts = Post.objects.filter(datetime_creation__gte=seven_days_ago, datetime_creation__lte=now)

    for post in posts:
        for category in post.categories.all():
            emails = User.objects.filter(
                subscriber__category=category
            ).values_list('email', flat=True)
            for email in emails:
                if email not in emails_users:
                    emails_users[email] = set()
                emails_users[email].add(post)

    for email, posts in emails_users.items():
        subject = 'Дайджест по понедельникам!'
        text = 'Пришло время прочитать посты из ваших любимых категорий!'
        html = '<b>Пришло время прочитать посты из ваших любимых категорий!</b>'
        for post in posts:
            text += f'\n{post.title} - http://127.0.0.1:8000/{post.get_absolute_url()}'
            html += f'<br><a href="http://127.0.0.1:8000/{post.get_absolute_url()}">{post.title}</a>,'
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()