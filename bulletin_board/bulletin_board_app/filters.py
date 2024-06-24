from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter

from .models import Response, Category, Announcement


class ResponseFilter(FilterSet):
    announcement_category = ModelMultipleChoiceFilter(
        field_name='announcement__category',
        queryset=Category.objects.all(),
        label='Категория (множественный выбор Ctrl+ЛКМ)',
    )
    announcement_title = CharFilter(
        field_name='announcement__title',
        lookup_expr='icontains',
        label='Заголовок объявления содержит',
    )
    text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Сообщение от пользователя содержит',
    )

    class Meta:
        model = Response
        fields = {}


class AnnouncementFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория (множественный выбор Ctrl+ЛКМ)',
    )
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок объявления содержит',
    )

    class Meta:
        model = Announcement
        fields = {}
