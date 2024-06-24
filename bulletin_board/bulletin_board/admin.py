from django.contrib import admin

from .models import *


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'category')


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Category, CategoryAdmin)
