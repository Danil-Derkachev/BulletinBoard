from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Announcement


@shared_task
def send_email_to_announcement_creator(announcement_pk):
    announcement = Announcement.objects.get(pk=announcement_pk)
    announcement_creator_email = set(announcement.user.email)
    text_content = f'Кто-то откликнулся на твоё объявление: {announcement.title}'
    html_content = render_to_string('celery_email.html', {'title': announcement.title})
    msg = EmailMultiAlternatives(
        subject='Кто-то откликнулся!',
        body=text_content,
        from_email='random@example.com',
        to=announcement_creator_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
