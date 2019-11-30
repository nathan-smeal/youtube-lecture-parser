"""Tests that data classes are set properly
"""
import pytest

from q_generator import popo


class TestPopoClass:
    def test_question_init(self):
        """This tests the simple question data class
        """
        inputs = {"question": "Question Text", "answer": "test answer"}
        popo.Question(**inputs)
