from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from .models import *
from .forms import *
from .tasks import *
from .filters import *


class AnnouncementsList(ListView):
    model = Announcement
    template_name = 'bulletin_board/list_announcements.html'
    context_object_name = 'list_announcements'
    paginate_by = 3
    ordering = '-datetime'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnnouncementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AnnouncementDetail(DetailView):
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


class ResponsesList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'bulletin_board/list_responses.html'
    context_object_name = 'list_responses'
    paginate_by = 3
    ordering = '-datetime'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['responses'] = Response.objects.filter(announcement__user=self.request.user.id)
        return context


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'bulletin_board/delete_response.html'
    success_url = reverse_lazy('list_responses')


@login_required
def accept_response(request, **kwargs):
    response = Response.objects.get(pk=kwargs['pk'])
    if response:
        response.accept()
        send_email_to_response_creator.apply_async([kwargs['pk']])
    return redirect('list_responses')

