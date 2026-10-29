import json
import os
import sys

import cv2
import numpy as np
import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from math_class import MathClass
from pipeline_class import PipelineClass
from setup_class import SetupClass


def _isStub(func):
    def reference(self):
        pass
    return func.__code__.co_code == reference.__code__.co_code


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "needs_steps(*names): skipped while these PipelineClass methods are still stubs")


def pytest_collection_modifyitems(config, items):
    for item in items:
        for marker in item.iter_markers("needs_steps"):
            for name in marker.args:
                if _isStub(getattr(PipelineClass, name)):
                    item.add_marker(pytest.mark.skip(
                        reason="PipelineClass.%s() is still a stub" % name))


class StubDisplay(object):

    def __init__(self):
        self.calls = []

    def setScreen(self, index):
        self.calls.append(("setScreen", index))

    def setFullscreen(self, enabled=True):
        self.calls.append(("setFullscreen", enabled))

    def show(self, frame):
        self.calls.append(("show", frame))

    def waitKey(self, delayMs=0):
        self.calls.append(("waitKey", delayMs))
        return 27

    def close(self):
        self.calls.append(("close",))


@pytest.fixture
def stubDisplay():
    return StubDisplay()


@pytest.fixture
def makeSettings(tmp_path):
    def make(side="LEFT", resXY=(200, 60), w=100.0, d=80.0, gamma=1.0,
             sourceSize=None, name=None):
        resX, resY = resXY
        if sourceSize is None:
            sourceSize = (2 * resX - MathClass.overlapPx(resX, w, d), resY)
        sourceW, sourceH = sourceSize
        rng = np.random.default_rng(12345)
        picture = rng.integers(0, 256, size=(sourceH, sourceW, 3), dtype=np.uint8)
        assert cv2.imwrite(str(tmp_path / "source.png"), picture)
        settings = {
            "projectorResXY": [resX, resY],
            "imageWidthCm": w,
            "projectorSpacingCm": d,
            "blendCurveGamma": gamma,
            "sourcePath": "source.png",
            "projectorSide": side,
        }
        path = tmp_path / (name or "settings.%s.json" % str(side).lower())
        path.write_text(json.dumps(settings), encoding="utf-8")
        return str(path)
    return make


@pytest.fixture
def loadSetup():
    def load(path):
        setup = SetupClass()
        setup.load(path)
        assert setup.validate()
        return setup
    return load


@pytest.fixture
def makePipeline(makeSettings, loadSetup):
    def make(side="LEFT", **kwargs):
        return PipelineClass(loadSetup(makeSettings(side=side, **kwargs)))
    return make


SIZE_CASES = [
    pytest.param(200, 60, 100.0, 80.0, 40, id="even40"),
    pytest.param(200, 60, 100.0, 90.0, 20, id="even20"),
    pytest.param(200, 60, 100.0, 89.5, 21, id="odd21"),
    pytest.param(200, 60, 100.0, 84.5, 31, id="odd31"),
    pytest.param(1920, 1080, 100.0, 80.0, 384, id="realistic384"),
]
