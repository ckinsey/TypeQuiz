from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import simplejson
from django.core.urlresolvers import reverse

from typequiz.typing_test.models import TypingTest, TestResult
from typequiz.typing_test.forms import TypingTestForm

import re
import difflib


def homepage(request):
    tmpl = "index.html"
    tests = TypingTest.objects.all()

    context = {
        'tests': tests,
    }

    return render(request, tmpl, context)

def quiz(request, slug):
    tmpl = "quiz.html"

    quiz = get_object_or_404(TypingTest, slug=slug)

    if request.POST and request.is_ajax():
        # Inbound data is in ms, so lets format that
        #start_time = _ms_to_s(request.POST.get('start_time'))
        #end_time = _ms_to_s(request.POST.get('end_time'))
        total_time = _ms_to_s(request.POST.get('total_time'))
        user_test_text = request.POST.get('user_test_text')

        # Check test accuracy
        errors = _check_test_accuracy(quiz.test_body, user_test_text)


        # Create result
        test_result = TestResult(total_time=total_time, typing_test=quiz,
            errors=errors, total_chars=len(user_test_text))

        test_result.save()

        out_data = {
            'wpm': test_result.get_wpm(),
            'errors': test_result.errors,
            'nwpm': test_result.get_nwpm(),
            'results': reverse("test_result", args=[test_result.id]),
        }
        return HttpResponse(simplejson.dumps(out_data), mimetype='application/json')

    context = {
        'obj': quiz,
        'form': TypingTestForm()
    }

    return render(request, tmpl, context)

def test_result(request, id):
    tmpl = "test_result.html"
    test_result = get_object_or_404(TestResult, id=id)

    context = {
        'test_result': test_result
    }

    return render(request, tmpl, context)


def _ms_to_s(ms):
    return int(ms) / 1000


def _check_test_accuracy(test_text, user_text):
    """
    Compares user_text to the original test_text, and determines the number of typing errors present
    """

    # Normalize whitespace
    test_text_normalized = re.sub(r'\s+', ' ', test_text)
    user_text_normalized = re.sub(r'\s+', ' ', user_text)

    # Split into arrays
    test_words = test_text_normalized.split(" ")
    user_words = user_text_normalized.split(" ")

    print user_words

    total_errors = 0

    # Go word-by-word
    for x in xrange(len(test_words)):
        try:
            # Are the words equal?
            if test_words[x] == user_words[x]:
                continue
            else:
                total_errors += 1
        except IndexError:
            # He ran out of time :(
            break

    return total_errors