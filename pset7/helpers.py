from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    # generate sets of lines for each input string (remove duplicates)
    lines_a = set(a.splitlines())
    lines_b = set(b.splitlines())

    # initialize empty set to store identical lines
    same = set()

    # check for identical lines
    for line in lines_a:
        if line in lines_b:

            # add identical lines to a set
            same.add(line)

    return list(same)


def sentences(a, b):
    """Return sentences in both a and b"""

    # generate sets of sentences for each input string (remove duplicates)
    sent_a = set(sent_tokenize(a, language='english'))
    sent_b = set(sent_tokenize(b, language='english'))

    # initialize empty set to store identical sentences
    same = set()

    # check for identical sentences
    for sent in sent_a:
        if sent in sent_b:

            # add identical sentences to a set
            same.add(sent)

    return list(same)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # initialize lists of substrings
    substr_a = []
    substr_b = []

    # generate substrings for string a
    for i in range(len(a) - (n - 1)):
        j = i + n
        substr = a[i:j]
        substr_a.append(substr)

    # generate substrings for string b
    for k in range(len(b) - (n - 1)):
        l = k + n
        substr = b[k:l]
        substr_b.append(substr)

    # initiliaze set to hold identical substrings
    same = set()

    # add identical substrings to a set
    for sub in set(substr_a):
        if sub in set(substr_b):
            same.add(sub)

    return list(same)
