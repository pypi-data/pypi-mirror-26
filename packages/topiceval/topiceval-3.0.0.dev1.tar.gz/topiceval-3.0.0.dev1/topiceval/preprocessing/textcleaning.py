"""
This module implements text cleaning, with multiple regex for filetring numbers,
weekday/weekend day names, money values, urls, emails etc.
Some emails specific regex is also present and is marked via comments, and
can be removed so that this module can be used for general text cleaning.
"""

from __future__ import division
from __future__ import print_function

from topiceval.preprocessing import params

try:
    from nltk.stem.wordnet import WordNetLemmatizer
except ImportError:
    WordNetLemmatizer = None

import re


def get_shorter_lem_word(word, lemma=WordNetLemmatizer()):
    try:
        nword = lemma.lemmatize(word, 'n')
        if len(nword) < len(word):
            return nword
        vword = lemma.lemmatize(word, 'v')
        if len(vword) < len(word):
            return vword
        else:
            return word
    except Exception as e:
        print('Exception during lemmatization for word: %s' % word)
        print(e)
        return word


def clean_text(text):
    """ Return clean text """

    # Check if lemmatizer is available (from NLTK), and instantiate lemma accordingly
    if WordNetLemmatizer is not None:
        # noinspection PyBroadException
        try:
            lemma = WordNetLemmatizer()
            lemma.lemmatize('test_word', 'n')
        except:
            lemma = None
    else:
        lemma = None

    # text = re.sub(r'\r', '', text)
    # text = re.sub(r'^On (Sun|Mon|Tue|Wed|Thu|Fri|Sat).*?wrote:$', ' ', text, flags=re.DOTALL | re.MULTILINE)
    # Lowercase the entire text
    text = text.lower()
    # Remove any '<' or '>' chars. This is to identify <> tags easily afterwards
    text = re.sub(r'[<>]', ' ', text)
    # Only ascii characters, replace others by ' '
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    # Replace metadata info by <meta> tag
    text = re.sub(r'(^to:.*)|(^from: .*)|(^cc:.*)|(^bcc:.*)|(^subject:.*)|(^sent:.*)|(^sent by:.*)|(^when:.*)|'
                  r'(^where:.*)|(^date: .*)', '<meta>', text,
                  flags=re.MULTILINE)                       # email specific
    # Remove any text which follows "-----Original ..-----" since it is a copy of original mail text
    text = re.sub(r'-{5}original .*?-{5}', ' ', text)       # email specific
    text = re.sub(r'-{5,10} forwarded message -{5,10}', ' ', text)  # email specific
    # Remove a line that starts with 10 or more special characters and content after it
    text = re.sub(r'^[^a-z0-9 \n]{10,}?$.*?(<meta>)', ' ', text, flags=re.DOTALL | re.MULTILINE)  # email specific
    text = re.sub(r'^[^a-z0-9 \n]{10,}?$.*', ' ', text, flags=re.DOTALL | re.MULTILINE)
    # Replace email addresses with tag <email>
    text = re.sub(r'[^@ ]+@[^@ ]+\.[^@ ]+', ' <email> ', text)
    # Replace some identifiable url's with <url> tag
    text = re.sub(r'http://[^ \n]+', ' <url> ', text)
    text = re.sub(r'https://[^ \n]+', ' <url> ', text)
    text = re.sub(r'www\.[^ \n]+', ' <url> ', text)
    # Replace weekday names with <weekday> tag
    text = re.sub(r'([^a-z]|^)(monday|mon|tuesday|tue|wednesday|wed|thursday|thu|friday|fri)([^a-z]|$)',
                  ' \g<1><weekday>\g<3> ', text, flags=re.MULTILINE)
    text = re.sub(r'([^a-z]|^)(saturday|sunday)([^a-z]|$)', ' \g<1><weekend>\g<3> ', text, flags=re.MULTILINE)
    text = re.sub(r'([^a-z]|^)(january|jan|february|feb|march|april|apr|june|jun|july|jul|august|aug|september|sept'
                  r'|october|oct|november|nov|december|dec)([^a-z]|$)', ' \g<1><month>\g<3> ', text, flags=re.MULTILINE)
    text = re.sub(r'([0-9]{1,2}:[0-9]{2}( ?)(am|pm|noon|afternoon|evening|morning|night)?)|(\d{1,2}( ?)'
                  r'(am|pm|noon|afternoon|evening|morning|night))', ' <time> ', text)
    text = re.sub(r'(dd/mm/yy)|(\d+/\d+/\d+)|(<month> \d{1,2}(st|nd|rd|th)?)', ' <date> ', text)
    text = re.sub(r'(\$|rs\.?)( ?)[0-9]+', ' <money> ', text)
    text = re.sub(r'([^a-z]|^)[0-9]+([^a-z]|$)', '\g<1><number>\g<2> ', text)
    text = re.sub(r'[^a-zA-Z<>_\-]', ' ', text)
    text = re.sub(r'-{2,}|_{2,}', ' ', text)
    text = re.sub(r'-[^a-z<>]|[^a-z<>]-', ' ', text)
    words = text.split()

    if params.usenltk and lemma is not None:
        words = [get_shorter_lem_word(w, lemma) for w in words if (2 < len(w) < 20)]
    else:
        words = [w for w in words if 2 < len(w) < 20]

    return ' '.join(words)


def remove_stops(text, stop):
    """ Use extended list of stopwords and return text cleaned off them"""
    words = text.split()
    words = [w for w in words if w not in stop]
    return ' '.join(words)


def remove_signature(text):
    signatures = ["best", "thanking you", "thanks", "yours sincerely", "sincerely", "warm regards", "regards",
                  "best regards"]
    for signature in signatures:
        text = re.sub(r'^%s,[^a-z]*?$.*?(<meta>)' % signature, ' ', text,
                      flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
        text = re.sub(r'^%s,([^a-z]*?)$.*' % signature, ' ', text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    # for name in names:
    #     text = re.sub(r'^%s.*' % name, ' ', text, flags=re.IGNORECASE)
    return text
