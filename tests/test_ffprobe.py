"""Test FFprobe utility functions."""

import json
import subprocess
from types import SimpleNamespace
from whisper_tiktok import utils


def make_subprocess_result(stdout: str, stderr: str = "", returncode: int = 0):
    """Creates a mock subprocess result for testing purposes.

    Args:
        stdout: The standard output of the subprocess.
        stderr: The standard error of the subprocess. Defaults to "".
        returncode: The return code of the subprocess. Defaults to 0.

    Returns:
        A SimpleNamespace object containing the stdout, stderr, and returncode.
    """
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def test_get_ffprobe_result_monkeypatched(monkeypatch):
    """Test get_ffprobe_result with monkeypatching.

    This test mocks the subprocess.run function to return a predefined JSON output,
    simulating the result of ffprobe. It then checks if the get_ffprobe_result function
    correctly parses this output and returns the expected values.
    """
    sample = {"streams": [{"codec_type": "video", "duration": "3.5", "width": 1280, "height": 720}]}
    fake_stdout = json.dumps(sample)

    def fake_run(cmd, stdout, stderr, universal_newlines, *args, **kwargs):
        return make_subprocess_result(stdout=fake_stdout)

    monkeypatch.setattr(subprocess, "run", fake_run)
    res = utils.get_ffprobe_result("dummy.mp4")
    assert res.return_code == 0
    assert json.loads(res.json)["streams"][0]["codec_type"] == "video"


def test_get_info_video(monkeypatch):
    """Test that get_info returns the correct video information."""
    ffprobe_json = {"streams": [{"codec_type": "video", "duration": "4.0", "width": 1920, "height": 1080}]}
    monkeypatch.setattr(
        utils,
        "get_ffprobe_result",
        lambda filename: utils.FFProbeResult(0, json.dumps(ffprobe_json), ""),
    )
    info = utils.get_info("dummy.mp4", "video")
    assert info["width"] == 1920
    assert info["height"] == 1080
    assert abs(info["duration"] - 4.0) < 1e-6
