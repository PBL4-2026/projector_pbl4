#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
import logging
import math

import cv2
import numpy as np

from display import Display, findProjectorScreens
from image import Image
from math_class import MathClass
from setup_class import SetupClass

_log = logging.getLogger(__name__)

# ˄


class PipelineClass(object):
    # ˅
    
    # ˄

    def load(self):
        # ˅
        # Image.load() raises FileNotFoundError / ValueError naming the path.
        path = self.__setup.getSourcePath()
        image = Image()
        image.load(path)
        self.__sourceFrame = image
        return image
        # ˄

    def crop(self):
        # ˅
        if self.__sourceFrame is None:
            raise ValueError("No source frame: call load() and scaleSource() first")

        frame = self.__sourceFrame.getFrame()
        if frame is None:
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
        frameWidth = frame.shape[1]

        if xStart < 0 or width <= 0 or xStart + width > frameWidth:
            raise ValueError(
                "Region (%d, %d) does not fit inside scaled source frame width %d"
                % (xStart, width, frameWidth)
            )

        # Return a copy wrapped in Image so applyMask() cannot modify sourceFrame.
        result = Image()
        result.setFrame(frame[:, xStart:xStart + width].copy())
        return result
        # ˄

    def applyMask(self, sliceFrame):
        # ˅
        if self.__mask is None:
            raise ValueError("No mask: the mask must be built before applyMask()")
        # The mask is built once elsewhere and only read here.
        alpha = np.asarray(self.__mask.getAlpha(), dtype=np.float64)
        frame = sliceFrame.getFrame()
        if frame.shape[1] != alpha.shape[0]:
            raise ValueError(
                f"Slice width {frame.shape[1]} does not match mask length {alpha.shape[0]}")
        # One multiplier per column, broadcast over rows and colour channels.
        scale = alpha.reshape((1, -1) + (1,) * (frame.ndim - 2))
        out = np.rint(frame.astype(np.float64) * scale)
        result = Image()
        result.setFrame(np.clip(out, 0, 255).astype(np.uint8))
        return result
        # ˄

    def display(self, frame):
        # ˅
        if not isinstance(frame, Image):
            raise ValueError(
                "frame must be an Image, got %s" % type(frame).__name__
            )

        array = frame.getFrame()
        if array is None:
            raise ValueError("frame is empty: call load() and scaleSource() first")

        screens, screenIndex = findProjectorScreens()
        display = Display(screens=screens, screen=screenIndex)
        try:
            display.show(array)
            display.setFullscreen(True)
            while display.waitKey(0) == -1:
                pass
        finally:
            display.close()

        self.__output = frame
        # ˄

    def run(self):
        # ˅
        # The region and mask were built once in the constructor.
        self.load()
        self.scaleSource()
        sliceFrame = self.crop()
        self.display(self.applyMask(sliceFrame))
        # ˄

    def scaleSource(self):
        # ˅
        if self.__sourceFrame is None:
            raise ValueError("No source frame: call load() first")
        src = self.__sourceFrame.getFrame()
        resX, resY = self.__setup.getProjectorResXY()
        overlapPx = self.__math.overlapPx(
            resX, self.__setup.getImageWidthCm(), self.__setup.getProjectorSpacingCm())
        # Combined image: both projectors side by side, minus the shared overlap.
        dstW, dstH = 2 * resX - overlapPx, resY
        srcH, srcW = src.shape[:2]
        # Keep the aspect ratio: scale until the picture covers the target on both
        # sides, then cut the extra from the centre. Nothing is stretched.
        scale = max(dstW / srcW, dstH / srcH)
        newW = max(dstW, math.ceil(srcW * scale - 1e-9))
        newH = max(dstH, math.ceil(srcH * scale - 1e-9))
        if (newW, newH) != (dstW, dstH):
            _log.info("Source aspect ratio %.3f differs from target %.3f; "
                      "the extra edges are cropped", srcW / srcH, dstW / dstH)
        interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
        resized = cv2.resize(src, (newW, newH), interpolation=interpolation)
        x0 = (newW - dstW) // 2
        y0 = (newH - dstH) // 2
        resized = resized[y0:y0 + dstH, x0:x0 + dstW].copy()
        scaled = Image()
        scaled.setFrame(resized)
        self.__sourceFrame = scaled
        return scaled
        # ˄

    def __init__(self, setup):

        self.__setup = None

        self.__math = None

        self.__sourceFrame = None

        self.__mask = None

        self.__output = None

        # ˅
        if setup is None or setup.getProjectorResXY() is None:
            raise ValueError("setup must be a loaded SetupClass: call load() and validate() first")
        self.__setup = setup
        self.__math = MathClass()
        resX = setup.getProjectorResXY()[0]
        w = setup.getImageWidthCm()
        d = setup.getProjectorSpacingCm()
        side = setup.getProjectorSide()
        self.__region = self.__math.cropRegion(side, resX, w, d)
        overlapPx = self.__math.overlapPx(resX, w, d)
        self.__mask = self.__math.blendMask(overlapPx, resX, side, setup.getBlendCurveGamma())
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
