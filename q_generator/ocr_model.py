"""This is a OCR with rule based model for finding question candidates.
"""
from .model import Model
from typing import List
from .popo import Question
from correlator.correlation import Correlation


class GrammarKbaiModel(Model):
    def __init__(self):
        super().__init__()

    def generate_questions(self) -> List[Question]:
        super().generate_questions
        return []

    def process_correlation(self, correlation: Correlation):
        return super().process_correlation(correlation)
