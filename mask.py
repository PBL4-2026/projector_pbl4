#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄

class Mask(object):
    """!
    @brief The brightness multipliers for one projector

    """

    # ˅
    
    # ˄
    
    @classmethod
    def getAlpha(self):
        """!"
        @brief Give the brghtnness multiples for the projector.
        @return list of float List of floats between 0 to 1, one per one pixel column.
        """

        # ˅
        return self.__alpha
        # ˄

    def __init__(self, alpha):

        """!
        @brief Initialize the Mask instance.
        @param alpha List of floats between 0 and 1, one per pixel column.
        """

        self.__alpha = None

        # ˅
        self.__alpha = alpha
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
