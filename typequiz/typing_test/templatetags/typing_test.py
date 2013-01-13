from django import template

from typequiz.typing_test.utils import check_test_accuracy, normalize_test_text

register = template.Library()

@register.simple_tag()
def display_test_result_text(test_result):
    original_test_text = test_result.typing_test.test_body

    # Check the test, get error indexes:
    errors, error_indexes = check_test_accuracy(original_test_text, test_result.user_text)

    normalized_text = normalize_test_text(test_result.user_text)
    output = ""

    for x in xrange(len(normalized_text)):
        if x in error_indexes:
            output += "<b class='text-error'>"
        output += normalized_text[x]
        if x in error_indexes:
            output += "</b>"
        output += " "

    return output