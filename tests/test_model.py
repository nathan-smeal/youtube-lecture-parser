import pytest
from q_generator.model import Model


class TestModel:
    def test_abstract_model(self):
        with pytest.raises(AssertionError):
            _ = Model().generate_questions()
