from django.urls import path

from .views import *


urlpatterns = [
    path('', AnnouncementsList.as_view(), name='list_announcements'),
    path('announcements/<int:pk>', AnnouncementDetail.as_view(), name='detail_announcement'),
    path('announcements/create', AnnouncementCreate.as_view(), name='create_announcement'),

    path('announcements/<int:pk>/responses/create', ResponseCreate.as_view(), name='create_response'),
    path('responses', ResponsesList.as_view(), name='list_responses'),
    path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='delete_response'),
    path('responses/<int:pk>/accept', accept_response, name='accept_response'),
]
