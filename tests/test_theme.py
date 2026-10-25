import json
import tempfile
import unittest
from pathlib import Path

from terminal_theme_lab.theme import COLOR_KEYS, load_theme, save_theme, validate_theme


class ThemeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.theme = {"name": "Test", **{key: "#123ABC" for key in COLOR_KEYS}}

    def test_validate_normalizes_colors(self) -> None:
        self.theme["red"] = "#abcdef"
        self.assertEqual(validate_theme(self.theme)["red"], "#ABCDEF")

    def test_validate_rejects_missing_color(self) -> None:
        del self.theme["cyan"]
        with self.assertRaisesRegex(ValueError, "missing colors: cyan"):
            validate_theme(self.theme)

    def test_save_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "theme.json"
            expected = save_theme(path, self.theme)
            self.assertEqual(load_theme(path), expected)
            self.assertEqual(json.loads(path.read_text()), expected)


if __name__ == "__main__":
    unittest.main()
