from pathlib import Path
import tempfile
import unittest

from sync_player import parse_lrc


class ParseLrcTest(unittest.TestCase):
    def write_lrc(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".lrc", encoding="utf-8", delete=False)
        tmp.write(content)
        tmp.close()
        return Path(tmp.name)

    def test_parse_timestamped_lines(self):
        path = self.write_lrc("[00:01.50]First line\n[00:03.000]Second line\n")

        self.assertEqual(parse_lrc(path), [(1.5, "First line"), (3.0, "Second line")])

    def test_skip_metadata_and_empty_lines(self):
        path = self.write_lrc("[ar:Artist]\n[00:01.00]Hello\n[00:02.00]   \nplain text\n")

        self.assertEqual(parse_lrc(path), [(1.0, "Hello")])

    def test_sort_lines_by_timestamp(self):
        path = self.write_lrc("[00:05.00]Later\n[00:01.00]Earlier\n")

        self.assertEqual(parse_lrc(path), [(1.0, "Earlier"), (5.0, "Later")])


if __name__ == "__main__":
    unittest.main()
