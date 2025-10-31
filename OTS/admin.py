from django.contrib import admin
from .models import Candidate, Question, Result

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'test_attempted', 'points')
    search_fields = ('username', 'name')
    ordering = ('username',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qid', 'que', 'ans')
    search_fields = ('que',)
    ordering = ('qid',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('resultid', 'username', 'date', 'time', 'attempt', 'right', 'wrong', 'points')
    list_filter = ('date', 'username')
    ordering = ('-date', '-time')
