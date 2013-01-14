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

    source_offset = 0
    user_offset = 0
    # Go word-by-word
    for x in xrange(len(test_words)):
        try:
            # Are the words equal?
            if test_words[x + source_offset] == user_words[x + user_offset]:
                continue
            else:
                total_errors += 1
                # Do the next words match?
                if test_words[x + source_offset + 1] != user_words[x + user_offset + 1]:
                    # Did they skip word?
                    source_offset += 1
                    if test_words[x + source_offset] != user_words[x + user_offset]:
                        # Did they mash two words together?
                        user_offset += 1
                        if test_words[x + source_offset] == user_words[x + user_offset]:
                            error_indexes.append(x + user_offset)
                else:
                    error_indexes.append(x + user_offset)


        except IndexError:
            # Didn't finish, or skipped some words
            break

    return total_errors, error_indexes

def normalize_test_text(text):
    # Normalize whitespace
    text_normalized = re.sub(r'\s+', ' ', text)
    return text_normalized.split(" ")

def _lookahead_errors(offset, words1, words2):
    """
    Given two lists of words, look ahead and compare the next ten words (directly, and skipping ahead one in each list)
    to determine the least amount of errors.  This will determine if the user either:  Mistyped a word, skipped a word,
    or merged two words

    err_map = []

    # User mistyped a word, test the next 10 (or until end of list)
    errs = 0
    err_indexes = []
    for x in xrange(min(10, len(words1) - 1)):
        try:
            if words1[x+1] == words2[x+1]:
                continue
            else:
                errs += errs
                err_indexes.append(x)
        except:
            break

    err_map.append((errs, err_indexes),)

    # User skipped a word, test the next 10 (or until end of list)
    errs = 0
    err_indexes = []
    for x in xrange(min(10, len(words1) - 1)):
        try:
            if words1[x+1] == words2[x]:
                continue
            else:
                errs += errs
                err_indexes.append(x)
        except:
            break

    err_map.append((errs, err_indexes),)

    # User merged two words, test the next 10 (or until end of list)
    errs = 0
    err_indexes = []
    for x in xrange(min(10, len(words1))):
        try:
            if words1[x] == words2[x+1]:
                continue
            else:
                errs += errs
                err_indexes.append(x)
        except:
            break

    err_map.append((errs, err_indexes),)

    # Determine which case yields the least errors:
    least_error_index = 0
    least_errors = 10

    for i in xrange(len(err_map)):
        if err_map[i][0] < least_errors:
            least_errors = err_map[i][0]
            least_error_index = i

    return err_map[i][0], err_map[i][1],
    """

