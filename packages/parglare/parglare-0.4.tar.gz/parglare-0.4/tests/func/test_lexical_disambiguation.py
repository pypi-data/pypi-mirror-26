# -*- coding: utf-8 -*-
"""Test lexical disambiguation strategy.

Longest-match strategy is first used. If more tokens has the same length
priority is given to the more specific match (i.e. str match over regex).
If ambiguity is still unresolved priority is checked as the last resort.
At the end disambiguation error is reported.

"""
from __future__ import unicode_literals
import pytest  # noqa
from parglare import Parser, Grammar
from parglare.exceptions import ParseError


called = [False, False, False]


def act_called(which_called):
    def _called(_, __):
        called[which_called] = True
    return _called


actions = {
    "First": act_called(0),
    "Second": act_called(1),
    "Third": act_called(2),
}


@pytest.fixture()
def cf():
    global called
    called = [False, False, False]


def test_priority(cf):

    grammar = """
    S: First | Second | Third;
    First: /\d+\.\d+/ {15};
    Second: '14.75';
    Third: /\d+\.75/;
    """

    g = Grammar.from_string(grammar)
    parser = Parser(g, actions=actions, debug=True)

    # Priority is used first
    parser.parse('14.75')
    assert called == [True, False, False]


def test_most_specific(cf):

    grammar = """
    S: First | Second | Third;
    First: /\d+\.\d+/;
    Second: '14';
    Third: /\d+/;
    """

    g = Grammar.from_string(grammar)
    parser = Parser(g, actions=actions, debug=True)

    # String match in rule Second is more specific than Third regexp rule.
    parser.parse('14')
    assert called == [False, True, False]


def test_most_specific_longest_match(cf):

    grammar = """
    S: First | Second | Third;
    First: '147';
    Second: '14';
    Third: /\d+/;
    """

    g = Grammar.from_string(grammar)
    parser = Parser(g, actions=actions, debug=True)

    # All three rules could match. First is tried first because it is
    # more specific (str match) and longest. It succeeds so other two
    # are not tried at all.
    parser.parse('147')
    assert called == [True, False, False]


def test_longest_match(cf):

    grammar = """
    S: First | Second | Third;
    First: /\d+\.\d+/;
    Second: '13';
    Third: /\d+/;
    """

    g = Grammar.from_string(grammar)
    parser = Parser(g, actions=actions)

    # If all matches are regexes of the same priority use longest match
    # disambiguation.
    parser.parse('14.17')
    assert called == [True, False, False]


def test_failed_disambiguation(cf):

    grammar = """
    S: First | Second | Third;
    First: /\d+\.\d+/ {15};
    Second: '14.7';
    Third: /\d+\.75/ {15};
    """

    g = Grammar.from_string(grammar)
    parser = Parser(g, actions=actions, debug=True)

    # All rules will match but First and Third have higher priority.
    # Both are regexes so longest match will be used.
    # Both have the same length.

    with pytest.raises(ParseError) as e:
        parser.parse('14.75')

    assert 'disambiguate' in str(e)
    assert 'First' in str(e)
    assert 'Second' not in str(e)
    assert 'Third' in str(e)


def test_longest_match_prefer(cf):

    grammar = """
    S: First | Second | Third;
    First: /\d+\.\d+/ {15};
    Second: '14.7';
    Third: /\d+\.75/ {15, prefer};
    """

    g = Grammar.from_string(grammar)
    parser = Parser(g, actions=actions)

    # All rules will match but First and Third have higher priority.
    # Both are regexes so longest match will be used.
    # Both have the same length but the third rule is preferred.

    parser.parse('14.75')
    assert called == [False, False, True]
