from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView

from .models import *
from .forms import *
from .tasks import *


class AnnouncementsList(ListView):
    model = Announcement
    template_name = 'bulletin_board/list_announcements.html'
    context_object_name = 'list_announcements'


class AnnouncementDetail(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'bulletin_board/detail_announcement.html'
    context_object_name = 'detail_announcement'


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'bulletin_board/create_announcement.html'

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.user = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'bulletin_board/create_response.html'
    success_url = '/'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.user = User.objects.get(id=self.request.user.id)
        response.announcement = Announcement.objects.get(id=self.kwargs['pk'])
        send_email_to_announcement_creator.apply_async([self.kwargs['pk']])
        return super().form_valid(form)

    # def get_success_url(self):
    #     success_url = reverse('detail_announcement', args=[self.request.GET["post_id"]])
    #     return success_url
