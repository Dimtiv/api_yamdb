from django_filters import FilterSet, filters

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('year', 'name', 'genre', 'category')
