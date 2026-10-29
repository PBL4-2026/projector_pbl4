import logging

import numpy as np
import pytest

from pipeline_class import PipelineClass
from side import Side


class StubSetup:
    def getProjectorResXY(self):
        return [1920, 1080]

    def getImageWidthCm(self):
        return 100.0

    def getProjectorSpacingCm(self):
        return 80.0

    def getBlendCurveGamma(self):
        return 1.0

    def getProjectorSide(self):
        return Side.LEFT


def make_pipeline(frame):
    p = PipelineClass(StubSetup())
    p._PipelineClass__sourceFrame = frame
    return p


def test_scales_to_combined_width():
    p = make_pipeline(np.zeros((50, 100, 3), np.uint8))
    out = p.scaleSource()
    assert out.shape == (1080, 3456, 3)
    assert out.dtype == np.uint8
    assert p._PipelineClass__sourceFrame is out


def test_shrinking_works():
    out = make_pipeline(np.zeros((2000, 6000, 3), np.uint8)).scaleSource()
    assert out.shape == (1080, 3456, 3)


def test_before_load_raises():
    with pytest.raises(ValueError):
        make_pipeline(None).scaleSource()


def test_other_aspect_ratio_warns(caplog):
    with caplog.at_level(logging.WARNING):
        out = make_pipeline(np.zeros((50, 100, 3), np.uint8)).scaleSource()
    assert out.shape == (1080, 3456, 3)
    assert any(r.levelno == logging.WARNING for r in caplog.records)


def test_matching_aspect_ratio_does_not_warn(caplog):
    with caplog.at_level(logging.WARNING):
        make_pipeline(np.zeros((1080, 3456, 3), np.uint8)).scaleSource()
    assert not caplog.records
