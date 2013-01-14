from django.shortcuts import render

from typequiz.typing_test.models import TypingTest, TestResult


def homepage(request):
    tmpl = "index.html"
    tests = TypingTest.objects.all()
    recent_results = TestResult.objects.all().order_by('-date_created')[:10]

    context = {
        'tests': tests,
        'recent_results': recent_results,
    }

    return render(request, tmpl, context)


def _ms_to_s(ms):
    return int(ms) / 1000

