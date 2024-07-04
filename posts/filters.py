from django.forms import DateTimeInput, DateInput
from django_filters import FilterSet, DateFromToRangeFilter, CharFilter, ChoiceFilter, DateTimeFilter, DateFilter
from django_filters.widgets import RangeWidget

from .models import Post


class NewsFilter(FilterSet):
    title = CharFilter(label='Название', lookup_expr='icontains')
    type_post = ChoiceFilter(label='Тип', choices=Post.POSITIONS)
    datetime_creation = DateFilter(
        field_name='datetime_creation',
        label='Дата',
        lookup_expr='gt',
        widget=DateInput(format='%d-%m-%Y', attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'type_post', 'datetime_creation']
