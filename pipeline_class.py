#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
import logging

import cv2
import numpy as np

from display import Display
from math_class import MathClass
from setup_class import SetupClass

_log = logging.getLogger(__name__)

# ˄


class PipelineClass(object):
    # ˅
    
    # ˄

    def load(self):
        # ˅
        pass
        # ˄

    def crop(self):
        # ˅
        if self.__sourceFrame is None:
            raise ValueError("No source frame: call load() and scaleSource() first")

        resX, _resY = self.__setup.getProjectorResXY()
        region = self.__math.cropRegion(
            self.__setup.getProjectorSide(),
            resX,
            self.__setup.getImageWidthCm(),
            self.__setup.getProjectorSpacingCm(),
        )
        xStart = region.getXStartPx()
        width = region.getWidthPx()
        frameWidth = self.__sourceFrame.shape[1]

        if xStart < 0 or width <= 0 or xStart + width > frameWidth:
            raise ValueError(
                "Region (%d, %d) does not fit inside scaled source frame width %d"
                % (xStart, width, frameWidth)
            )

        # Return a copy so applyMask() cannot modify sourceFrame.
        return self.__sourceFrame[:, xStart:xStart + width].copy()
        # ˄

    def applyMask(self, sliceFrame):
        # ˅
        if self.__mask is None:
            raise ValueError("No mask: the mask must be built before applyMask()")
        # The mask is built once elsewhere and only read here.
        alpha = np.asarray(self.__mask.getAlpha(), dtype=np.float64)
        if sliceFrame.shape[1] != alpha.shape[0]:
            raise ValueError(
                f"Slice width {sliceFrame.shape[1]} does not match mask length {alpha.shape[0]}")
        # One multiplier per column, broadcast over rows and colour channels.
        scale = alpha.reshape((1, -1) + (1,) * (sliceFrame.ndim - 2))
        out = np.rint(sliceFrame.astype(np.float64) * scale)
        return np.clip(out, 0, 255).astype(np.uint8)
        # ˄

    def display(self, frame):
        # ˅
        if not isinstance(frame, np.ndarray):
            raise ValueError(
                "frame must be a numpy.ndarray, got %s" % type(frame).__name__
            )

        display = Display()
        try:
            display.show(frame)
            display.setFullscreen(True)
            while display.waitKey(0) == -1:
                pass
        finally:
            display.close()

        self.__output = frame
        # ˄

    def run(self):
        # ˅
        pass
        # ˄

    def scaleSource(self):
        # ˅
        src = self.__sourceFrame
        if src is None:
            raise ValueError("No source frame: call load() first")
        resX, resY = self.__setup.getProjectorResXY()
        overlapPx = self.__math.overlapPx(
            resX, self.__setup.getImageWidthCm(), self.__setup.getProjectorSpacingCm())
        # Combined image: both projectors side by side, minus the shared overlap.
        dstW, dstH = 2 * resX - overlapPx, resY
        srcH, srcW = src.shape[:2]
        # The picture is stretched to the target size; warn when that distorts it.
        if abs(srcW / srcH - dstW / dstH) / (dstW / dstH) > 0.01:
            _log.warning(
                "Source aspect ratio %.3f differs from target %.3f by more than 1%%; "
                "the picture will be stretched", srcW / srcH, dstW / dstH)
        interpolation = cv2.INTER_AREA if dstW * dstH < srcW * srcH else cv2.INTER_LINEAR
        self.__sourceFrame = cv2.resize(src, (dstW, dstH), interpolation=interpolation)
        return self.__sourceFrame
        # ˄

    def __init__(self, setup):

        self.__setup = None

        self.__math = None

        self.__sourceFrame = None

        self.__mask = None

        self.__output = None

        # ˅
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
