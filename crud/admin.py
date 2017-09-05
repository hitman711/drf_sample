from django.contrib import admin

from . import models
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    """docstring for QuestionAdmin"""
    list_display = [
        'title',
        'private',
        'user'
    ]

class AnswerAdmin(admin.ModelAdmin):
    """docstring for AnswerAdmin"""
    list_display = [
        'body',
        'question',
        'user'
    ]

class TenantAdmin(admin.ModelAdmin):
    """docstring for TenantAdmin"""
    list_display = [
        'name',
        'api_key',
        'api_hits'
    ]

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Tenant, TenantAdmin)
