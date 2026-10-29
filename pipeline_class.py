#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
import logging

import cv2
import numpy as np

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
        pass
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
        pass
        # ˄

    def run(self):
        # ˅
        pass
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
        # The picture is stretched to the target size; warn when that distorts it.
        if abs(srcW / srcH - dstW / dstH) / (dstW / dstH) > 0.01:
            _log.warning(
                "Source aspect ratio %.3f differs from target %.3f by more than 1%%; "
                "the picture will be stretched", srcW / srcH, dstW / dstH)
        interpolation = cv2.INTER_AREA if dstW * dstH < srcW * srcH else cv2.INTER_LINEAR
        scaled = Image()
        scaled.setFrame(cv2.resize(src, (dstW, dstH), interpolation=interpolation))
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
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
