"""
"""
import random
from django.db import models
from django.contrib.auth.models import User

def random_string():
    return str(random.randint(10000, 99999))

# Create your models here.
class Question(models.Model):
    """
    Question model
    Define the attributes of Question
    """
    title = models.CharField(max_length=300)
    private = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'Question'

    def __str__(self):
        return self.title

class Answer(models.Model):
    """
    Answer model
    Define the attributes of Answer
    """
    body = models.TextField()
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'Answer'

class Tenant(models.Model):
    """
    Tenant model
    Define the attributes of Tenant
    """
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, default=random_string)
    api_hits = models.IntegerField(default=0)

    class Meta:
        db_table = 'Tenant'

    def update_api_hit(self):
        """ Update API hit count by 1
        """
        self.api_hits = self.api_hits + 1
        self.save()
