from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from django.core.urlresolvers import reverse

from typequiz.typing_test.models import TypingTest, TestResult
from typequiz.typing_test.forms import TypingTestForm
from typequiz.typing_test.utils import check_test_accuracy

def test_detail(request, slug):
    tmpl = "test_detail.html"

    quiz = get_object_or_404(TypingTest, slug=slug)

    if request.POST and request.is_ajax():
        # Inbound data is in ms, so lets format that
        #start_time = _ms_to_s(request.POST.get('start_time'))
        #end_time = _ms_to_s(request.POST.get('end_time'))
        total_time = _ms_to_s(request.POST.get('total_time'))
        user_test_text = request.POST.get('user_test_text')

        # Check test accuracy
        errors, error_indexes = check_test_accuracy(quiz.test_body, user_test_text)


        # Create result
        test_result = TestResult(total_time=total_time, typing_test=quiz, user_text=user_test_text,
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
