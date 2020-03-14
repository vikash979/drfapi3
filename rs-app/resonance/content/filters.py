import django_filters
from .models import Question

class QuestionFilter(django_filters.FilterSet):
    question_type = django_filters.NumberFilter(lookup_expr='exact')
    difficulty = django_filters.NumberFilter(lookup_expr='exact')
    source = django_filters.NumberFilter(lookup_expr='exact')

    model = Question
    fields = ['question_type', 'source', 'difficulty']
