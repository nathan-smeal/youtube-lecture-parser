"""This file takes in a transcript object and question candidates.
This is the common piece to be used by generators.
"""
from typing import List
from .model import Model
from .popo import BaseQuestion, Question, Flashcard
from correlator.correlation import Correlation


class QuestionGenerator(object):
    def __init__(self, models: List[Model]):
        self.models = models

    def start(self):
        # starts the nlp model for the generation process
        for m in self.models:
            m.start()

    def stop(self):
        for m in self.models:
            m.stop()

    def generate_questions(
        self, inputs: List[Correlation], top_num=10
    ) -> List[BaseQuestion]:
        result = []
        # todo make this async gather
        for i in inputs:
            for m in self.models:
                result.append(m.process_correlation(i))
        return result[:-top_num]
