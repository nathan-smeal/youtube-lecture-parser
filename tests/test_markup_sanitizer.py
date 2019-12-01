from q_generator.simple_nlp import remove_markup


class TestMarkupSanitizer:
    def test_bracket_removal(self):
        test_input = "[narrator] actual text"
        expected = " actual text"
        actual = remove_markup(test_input)
        assert expected == actual, f"{actual} did not match expected:  {expected}"

    def test_astericks_removal(self):
        test_input = "*narrator* actual text"
        expected = " actual text"
        actual = remove_markup(test_input)
        assert expected == actual, f"'{actual}' did not match expected:  '{expected}'"
