"""Test utility functions."""

from pathlib import Path

from whisper_tiktok import utils


def test_convert_time_simple():
    """Test the convert_time function with simple values.

    It checks the conversion of 0, 1.234, and 3661.5 seconds to the expected "HH:MM:SS.MS" format.
    """
    assert utils.convert_time(0) == "00:00:00.000"
    assert utils.convert_time(1.234) == "00:00:01.234"
    assert utils.convert_time(3661.5) == "01:01:01.500"


def test_rgb_to_bgr():
    """Tests the rgb_to_bgr function."""
    assert utils.rgb_to_bgr("FFF000") == "00F0FF"
    assert utils.rgb_to_bgr("123456") == "563412"


def test_random_background(tmp_path):
    """Test that random_background returns a path to an existing file
    inside the given folder.
    """
    folder = tmp_path / "bg"
    folder.mkdir()
    f1 = folder / "a.mp4"
    f2 = folder / "b.mp4"
    f1.write_text("x")
    f2.write_text("y")
    res = utils.random_background(str(folder))
    assert Path(res).exists()
