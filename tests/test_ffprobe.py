import json
import subprocess
from types import SimpleNamespace
import pytest
from Whisper_TikTok import utils

def make_subprocess_result(stdout: str, stderr: str = "", returncode: int = 0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)

def test_get_ffprobe_result_monkeypatched(monkeypatch):
    sample = {"streams":[{"codec_type":"video","duration":"3.5","width":1280,"height":720}]}
    fake_stdout = json.dumps(sample)
    def fake_run(cmd, stdout, stderr, universal_newlines):
        return make_subprocess_result(stdout=fake_stdout)
    monkeypatch.setattr(subprocess, "run", fake_run)
    res = utils.get_ffprobe_result("dummy.mp4")
    assert res.return_code == 0
    assert json.loads(res.json)["streams"][0]["codec_type"] == "video"

def test_get_info_video(monkeypatch):
    ffprobe_json = {"streams":[{"codec_type":"video","duration":"4.0","width":1920,"height":1080}]}
    monkeypatch.setattr(utils, "get_ffprobe_result", lambda filename: utils.FFProbeResult(0, json.dumps(ffprobe_json), ""))
    info = utils.get_info("dummy.mp4", "video")
    assert info["width"] == 1920
    assert info["height"] == 1080
    assert abs(info["duration"] - 4.0) < 1e-6