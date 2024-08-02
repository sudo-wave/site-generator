import unittest

from main import extract_markdown_links


class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to netflix](https://www.netflix.com) and [to youtube](https://www.youtube.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to netflix", "https://www.netflix.com"),
                ("to youtube", "https://www.youtube.com"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
