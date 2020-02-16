from django.contrib import admin

from questions.models import TestAnswer, Question

admin.site.register(TestAnswer)
admin.site.register(Question)
