from pathlib import Path
import tempfile
import unittest

from sync_player import parse_lrc


class ParseLrcTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_lrc(self, content: str, encoding: str = "utf-8") -> Path:
        path = self.root / "lyrics.lrc"
        path.write_text(content, encoding=encoding)
        return path

    def test_parse_timestamped_lines(self):
        path = self.write_lrc("[00:01.50]First line\n[00:03.000]Second line\n")

        self.assertEqual(parse_lrc(path), [(1.5, "First line"), (3.0, "Second line")])

    def test_parse_multiple_timestamps_for_one_line(self):
        path = self.write_lrc("[00:01.00][00:05.25]Repeated chorus\n")

        self.assertEqual(
            parse_lrc(path),
            [(1.0, "Repeated chorus"), (5.25, "Repeated chorus")],
        )

    def test_parse_fraction_lengths_and_colon_separator(self):
        path = self.write_lrc(
            "[00:01.5]Tenths\n[00:02.25]Hundredths\n[00:03:125]Milliseconds\n"
        )

        self.assertEqual(
            parse_lrc(path),
            [(1.5, "Tenths"), (2.25, "Hundredths"), (3.125, "Milliseconds")],
        )

    def test_skip_metadata_plain_text_and_invalid_timestamps(self):
        path = self.write_lrc(
            "[ar:Artist]\n[00:01.00]Hello\n[00:99.00]Invalid\nplain text\n"
        )

        self.assertEqual(parse_lrc(path), [(1.0, "Hello")])

    def test_preserve_timestamped_empty_line(self):
        path = self.write_lrc("[00:01.00]Hello\n[00:02.00]   \n[00:03.00]World\n")

        self.assertEqual(
            parse_lrc(path),
            [(1.0, "Hello"), (2.0, ""), (3.0, "World")],
        )

    def test_preserve_empty_line_with_multiple_timestamps(self):
        path = self.write_lrc("[00:02.00][00:04.00]\n")

        self.assertEqual(parse_lrc(path), [(2.0, ""), (4.0, "")])

    def test_apply_positive_offset_metadata(self):
        path = self.write_lrc("[offset:+500]\n[00:01.00]Delayed\n")

        self.assertEqual(parse_lrc(path), [(1.5, "Delayed")])

    def test_apply_negative_offset_regardless_of_tag_position(self):
        path = self.write_lrc("[00:01.00]Earlier\n[offset:-250]\n")

        self.assertEqual(parse_lrc(path), [(0.75, "Earlier")])

    def test_sort_lines_by_timestamp(self):
        path = self.write_lrc("[00:05.00]Later\n[00:01.00]Earlier\n")

        self.assertEqual(parse_lrc(path), [(1.0, "Earlier"), (5.0, "Later")])

    def test_read_utf8_bom(self):
        path = self.write_lrc("[00:00.00]Start\n", encoding="utf-8-sig")

        self.assertEqual(parse_lrc(path), [(0.0, "Start")])


if __name__ == "__main__":
    unittest.main()
