"""Tests that data classes are set properly
"""
import pytest

from q_generator import popo


class TestPopoClass:
    def test_question_init(self):
        """This tests the simple question data class
        """
        inputs = {"question": "Question Text", "answer": "test answer"}
        actual = popo.Question(**inputs)
        assert actual.answer == inputs['answer']
        assert actual.question == inputs['question']
        assert actual.frame == None
        assert actual.yt_link == ''
