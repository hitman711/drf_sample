"""
"""
from rest_framework import serializers
from . import models

class QuestionSerializer(serializers.ModelSerializer):
     """docstring for QuestionSerializer"""
     class Meta:
        model = models.Question
        fields = ('id', 'title')

class AnswerSerializer(serializers.ModelSerializer):
    """docstring for AnswerSerializer"""
    class Meta:
        model = models.Answer
        fields = ('id', 'body', 'user')


class QuestionRetriveSerializer(serializers.ModelSerializer):
    """docstring for QuestionRetriveSerializer"""
    answer = serializers.SerializerMethodField()
    class Meta:
        model = models.Question
        fields = ('id', 'title', 'answer')

    def get_answer(self, obj):
        answer = AnswerSerializer(
            models.Answer.objects.filter(
                question=self.instance.id
            ),
            many=True
        )
        return answer.data

