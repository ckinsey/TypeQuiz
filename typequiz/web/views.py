from django.shortcuts import render

from typequiz.typing_test.models import TypingTest


def homepage(request):
    tmpl = "index.html"
    tests = TypingTest.objects.all()

    context = {
        'tests': tests,
    }

    return render(request, tmpl, context)


def _ms_to_s(ms):
    return int(ms) / 1000

