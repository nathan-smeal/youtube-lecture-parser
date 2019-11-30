"""This is a KBAI or rule based model for finding question candidates.
"""
from .model import Model


class GrammarKbaiModel(Model):
    def __init__(self):
        super().__init__()
