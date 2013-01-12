from django.contrib import admin
from typequiz.typing_test.models import *

class TypingTestAdmin(admin.ModelAdmin):
    pass

class TestResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(TypingTest, TypingTestAdmin)
admin.site.register(TestResult, TestResultAdmin)