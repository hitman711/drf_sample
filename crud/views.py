""" API views list
  QuestionViews
  QuestionRetriveView
"""
from rest_framework import generics
from django_filters import rest_framework

from django.views.generic import ListView
from django.contrib.auth.models import User

from . import serializers, filters, authentication, models
# Create your views here.
from .throttling import CustomThrottle

class QuestionViews(generics.ListAPIView):
    """
    View the list of questions records
    """
    throttle_classes = (CustomThrottle,)
    authentication_classes = (authentication.TenantAuthentication,)
    serializer_class = serializers.QuestionSerializer
    model_class = serializer_class.Meta.model
    queryset = model_class.objects.all().exclude(private=True)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = filters.QuestionFilter

class QuestionRetriveView(generics.RetrieveAPIView):
    """
    View to retrive individual question record
    """
    authentication_classes = (authentication.TenantAuthentication,)
    serializer_class = serializers.QuestionRetriveSerializer
    model_class = serializer_class.Meta.model
    queryset = model_class.objects.all().exclude(private=True)
    filter_backends = (rest_framework.DjangoFilterBackend,)


class IndexView(ListView):
    """
    Dashboard views to show list of tenant and count of questions, answers
    """
    model = models.Tenant
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Related details to show on template
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        context['questions'] = models.Question.objects.count()
        context['answers'] = models.Answer.objects.count()
        context['users'] = User.objects.count()
        return context
