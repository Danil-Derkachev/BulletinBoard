from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Announcement, Response


@shared_task
def send_email_to_announcement_creator(announcement_pk):
    announcement = Announcement.objects.get(pk=announcement_pk)
    announcement_creator_email = [announcement.user.email]
    text_content = f'Кто-то откликнулся на твоё объявление: {announcement.title}'
    html_content = render_to_string(
        template_name='celery_email_to_announcement_creator.html',
        context={
            'title': announcement.title,
            'username': announcement.user.username
        }
    )
    msg = EmailMultiAlternatives(
        subject='Кто-то откликнулся!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=announcement_creator_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_to_response_creator(response_pk):
    response = Response.objects.get(pk=response_pk)
    response_creator_email = [response.user.email]
    text_content = f'Кто-то принял твой отклик: {response.text}'
    html_content = render_to_string(
        template_name='celery_email_to_response_creator.html',
        context={
            'text': response.text,
            'username': response.user.username
        }
    )
    msg = EmailMultiAlternatives(
        subject='Кто-то принял твой отклик!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=response_creator_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_for_all(template_name):
    users = User.objects.all().values('username', 'email')
    print(users)
    for user in users:
        username = user['username']
        email = user['email']
        text_content = f'Здравствуй, {username}! Это текстовая новостная рассылка.'
        html_content = render_to_string(
            template_name=template_name + '.html',
            context={
                'username': username,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Новостная рассылка',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
