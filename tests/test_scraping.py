from scraping import scraper
import pytest
import tempfile
from os import path


@pytest.mark.web_integration
class TestIntClass:
    def test_caption_dl(self):
        """This tests download functionality as integration test.
        Not a unit test.
        """

        with tempfile.TemporaryDirectory() as temp_d:
            # Wrap up video from Educational foundations
            test_url = "https://www.youtube.com/watch?time_continue=1&v=VK5b5ZQEI7M"
            assert scraper.capture_vid_captions(test_url, temp_d, "test")
            # check that video file exists
            assert path.exists(path.join(temp_d, "test", "test.mp4"))
            assert path.exists(path.join(temp_d, "test", "test.srt"))
