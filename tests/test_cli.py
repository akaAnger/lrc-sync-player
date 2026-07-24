import unittest

from sync_player import build_parser


class CliValidationTest(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def parse(self, *args: str):
        return self.parser.parse_args(list(args))

    def test_accept_finite_offset_and_nonnegative_cps(self):
        args = self.parse("song.mp3", "lyrics.lrc", "--offset", "-0.5", "--cps", "0")

        self.assertEqual(args.offset, -0.5)
        self.assertEqual(args.cps, 0.0)

    def test_reject_nonfinite_offset(self):
        for value in ("nan", "inf", "-inf"):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                self.parse("--offset", value)

    def test_reject_negative_cps(self):
        with self.assertRaises(SystemExit):
            self.parse("--cps", "-1")

    def test_reject_nonfinite_cps(self):
        for value in ("nan", "inf", "-inf"):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                self.parse("--cps", value)


if __name__ == "__main__":
    unittest.main()
