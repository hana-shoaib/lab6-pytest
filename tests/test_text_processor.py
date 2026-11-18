"""
Lab 6 - TextProcessor tests (student version)

Every test below starts with the annotation  @pytest.mark.skip(reason=TODO).
For each test:
    1. Remove the @pytest.mark.skip line.
    2. Replace `pass` with real test code.
    3. Run pytest and read the coverage report.

Each test here is one function that runs many times, once per row of its
@pytest.mark.parametrize table. Add a row = add a test case.

If one row fails because of a real bug in src/, document only that row:

    pytest.param("hello", "olleh",
                 marks=pytest.mark.xfail(reason="BUG #N: ...", strict=True)),
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.text_processor import TextProcessor

TODO = "TODO: remove this annotation once you write the test"

# Marks every test in this file. Run only these with:  pytest -m text
pytestmark = pytest.mark.text


# ---------------------------------------------------------------- fixtures

@pytest.fixture
def tp():
    """A TextProcessor for each test."""
    return TextProcessor()


# ----------------------------------------------------------------- reverse

@pytest.mark.parametrize("text, expected", [
    ("a", "a"),
    ("", ""),
    pytest.param(
        "hello",
        "olleh",
        marks=pytest.mark.xfail(
            reason="BUG: reverse() returns the original text instead of reversing it",
            strict=True
        )
    ),
    pytest.param(
        "ab",
        "ba",
        marks=pytest.mark.xfail(
            reason="BUG: reverse() returns the original text instead of reversing it",
            strict=True
        )
    ),
])
def test_reverse(tp, text, expected):
    """reverse(text) should equal expected."""
    assert tp.reverse(text) == expected


# ------------------------------------------------------------ count_vowels

@pytest.mark.parametrize("text, expected", [
    ("hello", 2),
    ("xyz", 0),
    ("", 0),
    pytest.param(
        "HELLO",
        2,
        marks=pytest.mark.xfail(
            reason="BUG: count_vowels() does not handle uppercase vowels",
            strict=True
        )
    ),
    pytest.param(
        "AEIOU",
        5,
        marks=pytest.mark.xfail(
            reason="BUG: count_vowels() does not handle uppercase vowels",
            strict=True
        )
    ),
])
def test_count_vowels(tp, text, expected):
    """count_vowels(text) should equal expected. It must ignore case."""
    assert tp.count_vowels(text) == expected


# ----------------------------------------------------------- is_palindrome

@pytest.mark.parametrize("text, expected", [
    ("racecar", True),
    ("hello", False),
    pytest.param(
        "race car",
        True,
        marks=pytest.mark.xfail(
            reason="BUG: is_palindrome() does not ignore spaces",
            strict=True
        )
    ),
    pytest.param(
        "RaceCar",
        True,
        marks=pytest.mark.xfail(
            reason="BUG: is_palindrome() does not ignore case",
            strict=True
        )
    ),
])
def test_is_palindrome(tp, text, expected):
    """is_palindrome(text) should be expected. It must ignore spaces and case."""
    assert tp.is_palindrome(text) == expected


# -------------------------------------------------------------- word_count

# -------------------------------------------------------------- word_count

@pytest.mark.parametrize("text, expected", [
    ("hello world", 2),
    ("i didn't eat breakfast today", 5),

    pytest.param(
        "hello   world",
        2,
        marks=pytest.mark.xfail(
            reason="BUG: word_count() counts extra spaces as words",
            strict=True
        )
    ),

    pytest.param(
        "   forwards and backwards   ",
        3,
        marks=pytest.mark.xfail(
            reason="BUG: word_count() counts leading and trailing spaces as words",
            strict=True
        )
    ),
])
@pytest.mark.edge
def test_word_count(tp, text, expected):
    """word_count(text) should equal expected."""
    assert tp.word_count(text) == expected
# -------------------------------------------------------- capitalize_words

@pytest.mark.parametrize("text, expected", [
    ("hello world", "Hello World"),
    ("PYTHON", "Python"),
    ("", ""),
])
def test_capitalize_words(tp, text, expected):
    """capitalize_words(text) should equal expected. (This method has no bug.)"""
    assert tp.capitalize_words(text) == expected


# ---------------------------------------------------------------- truncate

@pytest.mark.parametrize("text, max_length, expected", [
    ("Hello World", 5, "Hello..."),
    ("Hi", 5, "Hi..."),
    ("Hello", 5, "Hello..."),
])
@pytest.mark.edge
def test_truncate(tp, text, max_length, expected):
    """truncate(text, max_length) should equal expected."""
    assert tp.truncate(text, max_length) == expected