#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
from mask import Mask
from region import Region
from side import Side


# ˄


class MathClass(object):
    """!
    @brief Provides calculations for dual-projector image projection

    Calculates overlap width, combined projection width, pixel density,
    image regions, and blending masks.

    """
    
    # ˅
    
    # ˄

    @classmethod
    def overlapCm(cls, w, d):
        """!
        @brief Calculates the overlapped width between the two both projectors

        @param w Width of the projected image from one projector [cm]
        @param d Distance between the two projectors [cm]
        @return Width of the overlapping screen regions [cm]
        @rtype float

        """

        # ˅
        pass
        # ˄

    @classmethod
    def totalWidthCm(cls, w, d):
        """!
        @brief Calculates the total width covered by both projectors.

        @param w Width of the image projected by one projector [cm].
        @param d Distance between the two projectors [cm].
        @return Total width of the combined projection [cm].
        @rtype float

        """

        # ˅
        pass
        # ˄

    @classmethod
    def pxPerCm(cls, resX, w):
        """!
        @brief Calculates the horizontal pixel density of a projector.

        @param resX Horizontal resolution of one projector [px].
        @param w Width of the image projected by one projector [cm].
        @return Horizontal pixel density [px/cm].
        @rtype float

        """
        # ˅
        pass
        # ˄

    @classmethod
    def overlapPx(cls, resX, w, d):
        """!
        @brief Calculates the overlap width in whole pixels.

        Both computers must use the same overlap pixel value.

        @param resX Horizontal resolution of one projector [px].
        @param w Width of the image projected by one projector [cm].
        @param d Distance between the two projectors [cm].
        @return Width of the overlap region in whole pixels [px].
        @rtype int


        """
        # ˅
        pass
        # ˄

    @classmethod
    def cropRegion(cls, projectorSide, resX, w, d):
        """!
        @brief Determines which region of the combined image a projector displays.

        The LEFT and RIGHT projector regions together cover the combined image.

        @param projectorSide Side of the projector, LEFT or RIGHT.
        @param resX Horizontal resolution of one projector [px].
        @param w Width of the image projected by one projector [cm].
        @param d Distance between the two projectors [cm].
        @return Region of the combined image displayed by this projector.
        @rtype Region


        """
        # ˅
        pass
        # ˄

    @classmethod
    def blendMask(cls, overlapPx, resX, projectorSide, gamma):
        """!
        @brief Creates a blending mask for one projector.

        The mask maintains full brightness outside the overlap and
        fades brightness within the overlap. Gamma controls the shape
        of the fade.

        @param overlapPx Width of the overlap region in whole pixels [px].
        @param resX Horizontal resolution of one projector [px].
        @param projectorSide Side of the projector, LEFT or RIGHT.
        @param gamma Value controlling the shape of the fade.
        @return Blending mask containing brightness multipliers from 0 to 1.
        @rtype Mask


        """
        # ˅
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
