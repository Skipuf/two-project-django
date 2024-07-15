from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from posts.models import Post


@receiver(m2m_changed, sender=Post.categories.through)
def categories_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action != "post_add":
        return
    emails_set = set()
    for category_id in pk_set:
        category = model.objects.get(pk=category_id)
        emails = User.objects.filter(
            subscriber__category=category
        ).values_list('email', flat=True)
        emails_set.update(emails)
    if emails_set:
        subject = f'Новый пост в категориях: {", ".join([model.objects.get(pk=category_id).name for category_id in pk_set])}'
        text_content = (
            f'{instance.title}\n'
            f'{instance.content.split(" ")[:20:]}\n\n'
            f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'{instance.title}<br>'
            f'{instance.content.split(" ")[:20:]}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails_set:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
