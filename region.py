#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class Region(object):
    """!
    @brief A strip of the combined image that one projector shows
    """

    # ˅
    
    # ˄

    def getXStartPx(self):
        """!
        @brief Give the x start pixel for the projector.
        """

        # ˅
        return self.__xStartPx
        # ˄

    def getWidthPx(self):
        """!
        @brief Give the width pixel for the projector.

        """

        # ˅
        return self.__widthPx
        # ˄

    def __init__(self, xStartPx, widthPx):
        """!
        @param xStartPx first column [px]
        @param number of columns [px]
        """

        self.__xStartPx = None

        self.__widthPx = None

        # ˅
        self.__xStartPx = xStartPx
        self.__widthPx = widthPx
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
