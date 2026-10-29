"""PipelineClass.crop tests (D-18)."""
import numpy as np
import pytest

from math_class import MathClass
from pipeline_class import PipelineClass
from side import Side


class StubSetup:
    def __init__(self, side):
        self._side = side

    def getProjectorResXY(self):
        return [1920, 1080]

    def getImageWidthCm(self):
        return 100.0

    def getProjectorSpacingCm(self):
        return 80.0

    def getBlendCurveGamma(self):
        return 1.0

    def getProjectorSide(self):
        return self._side


def make_pipeline(frame, side=Side.LEFT):
    p = PipelineClass(StubSetup(side))
    p._PipelineClass__setup = StubSetup(side)
    p._PipelineClass__math = MathClass
    p._PipelineClass__sourceFrame = frame
    return p


def test_left_slice_is_first_columns():
    resX, resY = 1920, 1080
    overlap = MathClass.overlapPx(resX, 100.0, 80.0)
    width = 2 * resX - overlap
    frame = np.zeros((resY, width, 3), np.uint8)
    frame[:, :, 0] = np.arange(width, dtype=np.uint8)  # unique column values

    out = make_pipeline(frame, Side.LEFT).crop()

    assert out.shape == (resY, resX, 3)
    assert np.array_equal(out[:, :, 0], frame[:, :resX, 0])


def test_right_slice_is_last_columns():
    resX, resY = 1920, 1080
    overlap = MathClass.overlapPx(resX, 100.0, 80.0)
    width = 2 * resX - overlap
    frame = np.zeros((resY, width, 3), np.uint8)
    frame[:, :, 0] = np.arange(width, dtype=np.uint8)

    out = make_pipeline(frame, Side.RIGHT).crop()

    assert out.shape == (resY, resX, 3)
    assert np.array_equal(out[:, :, 0], frame[:, -resX:, 0])


def test_slices_share_exactly_overlap_columns():
    resX, resY = 1920, 1080
    overlap = MathClass.overlapPx(resX, 100.0, 80.0)
    width = 2 * resX - overlap
    frame = np.random.default_rng(0).integers(0, 256, (resY, width, 3), dtype=np.uint8)

    left = make_pipeline(frame, Side.LEFT).crop()
    right = make_pipeline(frame, Side.RIGHT).crop()

    assert left.shape[1] == resX
    assert right.shape[1] == resX
    assert np.array_equal(left[:, -overlap:], right[:, :overlap])


def test_returns_copy_and_sourceframe_unchanged():
    resX, resY = 1920, 1080
    overlap = MathClass.overlapPx(resX, 100.0, 80.0)
    width = 2 * resX - overlap
    frame = np.full((resY, width, 3), 200, np.uint8)
    before = frame.copy()

    out = make_pipeline(frame, Side.LEFT).crop()
    out[:] = 0

    assert np.array_equal(frame, before)
    assert out is not frame


def test_no_frame_raises():
    with pytest.raises(ValueError):
        make_pipeline(None, Side.LEFT).crop()


def test_region_does_not_fit_raises():
    resX = 1920
    # Frame is too narrow for the full resX-wide slice.
    frame = np.zeros((1080, resX - 1, 3), np.uint8)
    with pytest.raises(ValueError):
        make_pipeline(frame, Side.LEFT).crop()
