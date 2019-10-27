from scraping import scraper
import pytest
import tempfile


@pytest.mark.web_integration
class TestIntClass:
    def test_caption_dl(self):
        """This tests download functionality as integration test.
        Not a unit test.
        """

        with tempfile.TemporaryDirectory() as temp_d:
            # Wrap up video from Educational foundations
            test_url = "https://www.youtube.com/watch?time_continue=1&v=VK5b5ZQEI7M"
            assert scraper.capture_vid_captions(test_url, temp_d)
            # citizen's aaaarrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
        assert 0
