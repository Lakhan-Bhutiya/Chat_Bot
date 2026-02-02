from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import QuestionAnswer

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(ImportExportModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question', 'answer')
