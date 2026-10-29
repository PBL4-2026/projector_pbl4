#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Preview both projectors on one computer: run LEFT and RIGHT, join them, show the result.

python tools/preview_both.py settings.json [--save out.png] [--no-window]
"""
import argparse
import os
import sys

import cv2
import numpy as np

# Scripts in tools/ import modules from the repository root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from display import Display
from math_class import MathClass
from pipeline_class import PipelineClass
from setup_class import SetupClass
from side import Side

MAX_WINDOW_WIDTH = 1600


def renderSide(settingsPath, side=None):
    """Run the pipeline steps for one settings file, without opening a projector window.

    side: Side to use instead of the projectorSide in the file (None keeps the file's).
    """
    setup = SetupClass()
    setup.load(settingsPath)
    if side is not None:
        setup.setProjectorSide(side)
    if not setup.validate():
        raise ValueError("Invalid settings: %s" % settingsPath)
    pipeline = PipelineClass(setup)
    pipeline.load()
    pipeline.scaleSource()
    return setup, pipeline.applyMask(pipeline.crop()).getFrame()


def join(leftFrame, rightFrame, overlapPx):
    """Add the two pictures where they overlap, as the light of the two projectors does."""
    resY, resX = leftFrame.shape[:2]
    width = 2 * resX - overlapPx
    canvas = np.zeros((resY, width, 3), np.int32)
    canvas[:, :resX] += leftFrame
    canvas[:, resX - overlapPx:] += rightFrame
    return np.clip(canvas, 0, 255).astype(np.uint8)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Preview the LEFT and RIGHT pictures joined together.")
    parser.add_argument("left_file", help="settings file (LEFT if a second file is given)")
    parser.add_argument("right_file", nargs="?",
                        help="optional second settings file for RIGHT; without it the first "
                             "file is used for both sides")
    parser.add_argument("--save", metavar="PATH", help="also write the joined picture to this file")
    parser.add_argument("--no-window", action="store_true", help="do not open a window")
    args = parser.parse_args(argv)

    try:
        if args.right_file:
            leftSetup, leftFrame = renderSide(args.left_file)
            _, rightFrame = renderSide(args.right_file)
        else:
            leftSetup, leftFrame = renderSide(args.left_file, Side.LEFT)
            _, rightFrame = renderSide(args.left_file, Side.RIGHT)
        overlapPx = MathClass.overlapPx(
            leftSetup.getProjectorResXY()[0],
            leftSetup.getImageWidthCm(),
            leftSetup.getProjectorSpacingCm())
        joined = join(leftFrame, rightFrame, overlapPx)
    except (OSError, ValueError) as e:
        print("Cannot preview: %s" % e, file=sys.stderr)
        return 1

    if args.save:
        if not cv2.imwrite(args.save, joined):
            print("Cannot write %s" % args.save, file=sys.stderr)
            return 1
        print("saved %s (%dx%d, overlap %d px)" % (args.save, joined.shape[1], joined.shape[0], overlapPx))

    if not args.no_window:
        shown = joined
        if joined.shape[1] > MAX_WINDOW_WIDTH:
            scale = MAX_WINDOW_WIDTH / joined.shape[1]
            shown = cv2.resize(joined, (MAX_WINDOW_WIDTH, round(joined.shape[0] * scale)),
                               interpolation=cv2.INTER_AREA)
        display = Display(windowName="preview")
        try:
            display.show(shown)
            while display.waitKey(0) == -1:
                pass
        finally:
            display.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
