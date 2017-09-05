""" Filter list for curd model
  QuestionFilter
"""
import django_filters

from . import models

class QuestionFilter(django_filters.FilterSet):
    """Search and retrive data from Question records
    """
    class Meta:
        model = models.Question
        char_search_fields = [
            'exact',
            'contains',
            'in',
            'startswith',
            'icontains',
        ]
        fields = {
            "title": char_search_fields
        }
