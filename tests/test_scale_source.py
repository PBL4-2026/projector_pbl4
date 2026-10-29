"""PipelineClass.scaleSource tests (KAN-58)."""
import logging

import numpy as np
import pytest

from image import Image
from math_class import MathClass
from pipeline_class import PipelineClass


class StubSetup:
    def getProjectorResXY(self):
        return [1920, 1080]

    def getImageWidthCm(self):
        return 100.0

    def getProjectorSpacingCm(self):
        return 80.0


def make_pipeline(frame):
    p = PipelineClass(StubSetup())
    p._PipelineClass__setup = StubSetup()
    p._PipelineClass__math = MathClass
    if frame is not None:
        image = Image()
        image.setFrame(frame)
        frame = image
    p._PipelineClass__sourceFrame = frame
    return p


def test_scales_to_combined_width():
    # overlapPx = 384 -> 2 * 1920 - 384 = 3456
    p = make_pipeline(np.zeros((50, 100, 3), np.uint8))
    out = p.scaleSource()
    assert isinstance(out, Image)
    assert out.getShape() == (1080, 3456, 3)
    assert out.getFrame().dtype == np.uint8
    assert p._PipelineClass__sourceFrame is out


def test_shrinking_works():
    out = make_pipeline(np.zeros((2000, 6000, 3), np.uint8)).scaleSource()
    assert out.getShape() == (1080, 3456, 3)


def test_before_load_raises():
    with pytest.raises(ValueError):
        make_pipeline(None).scaleSource()


def test_other_aspect_ratio_warns(caplog):
    with caplog.at_level(logging.WARNING):
        out = make_pipeline(np.zeros((50, 100, 3), np.uint8)).scaleSource()
    assert out.getShape() == (1080, 3456, 3)
    assert any(r.levelno == logging.WARNING for r in caplog.records)


def test_matching_aspect_ratio_does_not_warn(caplog):
    with caplog.at_level(logging.WARNING):
        make_pipeline(np.zeros((1080, 3456, 3), np.uint8)).scaleSource()
    assert not caplog.records
