import re

def check_test_accuracy(test_text, user_text):
    """
    Compares user_text to the original test_text, and determines the number of typing errors present
    """

    # Split into arrays
    test_words = normalize_test_text(test_text)
    user_words = normalize_test_text(user_text)

    total_errors = 0
    error_indexes = []

    # Go word-by-word
    for x in xrange(len(test_words)):
        try:
            # Are the words equal?
            if test_words[x] == user_words[x]:
                continue
            else:
                total_errors += 1
                error_indexes.append(x)
        except IndexError:
            # Didn't finish, or skipped a word
            break

    return total_errors, error_indexes

def normalize_test_text(text):
    # Normalize whitespace
    text_normalized = re.sub(r'\s+', ' ', text)
    return text_normalized.split(" ")