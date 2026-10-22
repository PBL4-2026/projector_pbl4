#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
from math_class import MathClass
from setup_class import SetupClass


# ˄


class PipelineClass(object):
     """
    @brief Processes an image for dual-projector display.

    Loads the source image, scales it, crops the region for
    this projector, applies a blending mask, and displays the result.
    """
    # ˅
    # ˄

    def load(self):
        """
        @brief Loads the source image using the path in the settings.

        @return None
        """
        # ˅
        pass
        # ˄

    def crop(self):
        """
        @brief Crops the part of the scaled image for this projector.

        @return Image slice for this projector.
        """
        # ˅
        pass
        # ˄

    def applyMask(self, sliceFrame):
        """
        @brief Applies the blending mask to the cropped image.

        @param sliceFrame Image slice produced by crop().
        @return Image with the blending mask applied.
        """
        # ˅
        pass
        # ˄

    def display(self, frame):
        """
        @brief Displays the processed image on this projector.

        @param frame Image to display.
        @return None
        """
        # ˅
        pass
        # ˄

    def run(self):
         """
        @brief Runs the image-processing steps in order.

        Loads, scales, crops, applies the mask, and displays the image.
        Video support is optional; still images are required.

        @return None
        """
        # ˅
        pass
        # ˄

    def scaleSource(self):
      """
        @brief Resizes the source image to cover both projectors.

        The exact scaling method is still to be decided.

        @return None for now.
        """
        # ˅
        pass
        # ˄

    def __init__(self):
        """
        @brief Initializes the pipeline attributes.
        """

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
