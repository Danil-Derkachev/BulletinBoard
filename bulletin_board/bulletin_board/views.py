from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.core.cache import cache

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'bulletin_board/detail_announcement.html'
    context_object_name = 'detail_announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_already_responded'] = Response.objects.filter(
            announcement=self.kwargs['pk'],
            user=self.request.user.id
        ).values('announcement', 'user')
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'detail_announcement-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'detail_announcement-{self.kwargs["pk"]}', obj)
        return obj


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'bulletin_board/create_announcement.html'

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.user = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class AnnouncementEdit(LoginRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'bulletin_board/edit_announcement.html'


class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'bulletin_board/delete_announcement.html'
    success_url = reverse_lazy('list_announcements')


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'bulletin_board/create_response.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.user = User.objects.get(id=self.request.user.id)
        response.announcement = Announcement.objects.get(id=self.kwargs['pk'])
        send_email_to_announcement_creator.apply_async([self.kwargs['pk']])
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse(viewname='detail_announcement', args=[self.kwargs['pk']])
        return success_url


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
        context['responses'] = Response.objects.select_related('announcement').filter(
            announcement__user=self.request.user.id
        )
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

