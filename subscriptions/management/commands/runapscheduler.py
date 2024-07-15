import logging
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from posts.models import Post

logger = logging.getLogger(__name__)


def my_job():
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
        subject = 'Пятничный дайджест!'
        text = f'Пришло время прочитать посты из ваших любимых категорий!'
        html = f'<b>Пришло время прочитать посты из ваших любимых категорий!</b>'
        for post in posts:
            text += f'\n{post.title} - http://127.0.0.1:8000/{post.get_absolute_url()}'
            html += f'<br><a href="http://127.0.0.1:8000/{post.get_absolute_url()}">{post.title}</a>,'
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(
            #     day_of_week="tri", hour="18", minute="00"
            # ),
            trigger=CronTrigger(
                minute="29"
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
