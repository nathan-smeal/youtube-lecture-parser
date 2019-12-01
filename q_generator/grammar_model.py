"""This is a KBAI or rule based model for finding question candidates.
"""
from .model import Model
from typing import List
from .popo import Question


class GrammarKbaiModel(Model):
    def __init__(self):
        super().__init__()

    def generate_questions(self) -> List[Question]:
        super().generate_questions
        return []

    @staticmethod
    def get_if_then(text: str) -> List[Question]:
        return []
