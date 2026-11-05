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
    """!
    @brief Processes an image for dual-projector display.

    Loads the source image, scales it, crops the region for
    this projector, applies a blending mask, and displays the result.
    """

    # ˅
    
    # ˄

    def load(self):
        """!
        @brief Loads the source image using the path in the settings.

        @Returns the loaded Image.
        @rtype

        @throws
        @throws
        """
        
        # ˅
        # Image.load() raises FileNotFoundError / ValueError naming the path.
        path = self.__setup.getSourcePath()
        image = Image()
        image.load(path)
        self.__sourceFrame = image
        return image
        # ˄

    def crop(self):
        """!
        @brief Crops the part of the scaled image for this projector.

        @return  a copy. applyMask() .
        @rtype Image

        @throws
        """

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
        """!
        @brief Applies the blending mask to the cropped image.

        @param sliceFrame Image slice produced by crop().

        @return a new Image and does not change its input.
        @rtype image

        @throws
        """

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
        """!
        @brief Opens a full-screen window on the second screen if there is one (otherwise the only screen),
         waits for a key press, then closes it. 

        @param frame Image to display.
        @return None
        @rtype

        @throws
        """

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
        """!
        @brief Runs the image-processing steps in order.

        Loads, scales, crops, applies the mask, and displays the image.
        the mask and the region are built once, and that each computer shows one side.
        Still pictures only. Video is not supported.still images are required.

        @return None
        @rtype None

        @throws
        @throws
        """

        # ˅
        # The region and mask were built once in the constructor.
        self.load()
        self.scaleSource()
        sliceFrame = self.crop()
        self.display(self.applyMask(sliceFrame))
        # ˄

    def scaleSource(self):
        """!
        @brief Resizes the source image to cover both projectors.

        @Returns the scaled Image. It keeps the aspect ratio and cuts the extra edges 
        from the centre (“crop to fill”). It never stretches the picture. It writes an INFO message when it crops. 
        @rtype Image

        @throws
        """

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
        """!
        @brief Takes setup (a loaded SetupClass). Builds the math object, 
        the region and the mask once. Add @param setup.
        
        @param
        
        @return
        @rtype

        @throws
        """

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
