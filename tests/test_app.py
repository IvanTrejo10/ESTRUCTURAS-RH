from io import BytesIO
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from streamlit.testing.v1 import AppTest
from test_structures import CR_HEADER, VALES_HEADER, book_bytes, cr_row, vales_row

APP = Path(__file__).resolve().parents[1] / "app.py"


class Upload(BytesIO):
    name = "base.xlsx"


class AppTests(unittest.TestCase):
    def test_initial_page_runs_and_requires_a_base(self):
        app = AppTest.from_file(str(APP)).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(app.button(key="create_structures").disabled)

    def test_full_generation_and_stale_downloads_after_period_change(self):
        files = {
            "source_cr": Upload(book_bytes(CR_HEADER, [cr_row()])),
            "source_vales": Upload(book_bytes(VALES_HEADER, [vales_row()])),
        }
        with patch("streamlit.file_uploader", side_effect=lambda *args, **kwargs: files.get(kwargs["key"])):
            app = AppTest.from_file(str(APP)).run(timeout=30)
            app.button(key="create_structures").click().run(timeout=30)
            self.assertFalse(app.exception)
            self.assertEqual(len(app.session_state["generated"]["results"]), 2)
            self.assertFalse(app.session_state["generated"]["errors"])
            self.assertEqual([result.total for result in app.session_state["generated"]["results"]], [1, 1])
            previous_week = app.number_input(key="week").value
            app.number_input(key="week").set_value(1 if previous_week != 1 else 2).run(timeout=30)
            self.assertFalse(app.exception)
            self.assertTrue(any("Vuelve a crear" in element.value for element in app.info))
            self.assertFalse(app.get("download_button"))

    def test_bad_cr_does_not_prevent_valid_vales_output(self):
        files = {"source_cr": Upload(b"invalid"), "source_vales": Upload(book_bytes(VALES_HEADER, [vales_row()]))}
        with patch("streamlit.file_uploader", side_effect=lambda *args, **kwargs: files.get(kwargs["key"])):
            app = AppTest.from_file(str(APP)).run(timeout=30)
            app.button(key="create_structures").click().run(timeout=30)
            self.assertFalse(app.exception)
            results = app.session_state["generated"]["results"]
            self.assertEqual([result.kind for result in results], ["vales"])
            self.assertTrue(app.error)


if __name__ == "__main__":
    unittest.main()
