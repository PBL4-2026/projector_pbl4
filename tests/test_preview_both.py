"""tools/preview_both.py tests."""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))

import preview_both
from math_class import MathClass


def test_joined_picture_matches_the_combined_source(makeSettings, tmp_path):
    left = makeSettings("LEFT", resXY=(200, 60), d=89.5)
    right = makeSettings("RIGHT", resXY=(200, 60), d=89.5)
    out = tmp_path / "joined.png"

    assert preview_both.main([left, right, "--save", str(out), "--no-window"]) == 0

    joined = cv2.imread(str(out))
    source = cv2.imread(str(tmp_path / "source.png"))
    overlapPx = MathClass.overlapPx(200, 100.0, 89.5)
    assert joined.shape == (60, 2 * 200 - overlapPx, 3)
    assert np.abs(joined.astype(np.int32) - source.astype(np.int32)).max() <= 1


def test_missing_settings_file_exits_1(tmp_path, capsys):
    code = preview_both.main([str(tmp_path / "a.json"), str(tmp_path / "b.json"), "--no-window"])
    assert code == 1
    assert "Cannot preview" in capsys.readouterr().err
