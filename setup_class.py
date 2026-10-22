#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class SetupClass(object):
    # ˅
    
    # ˄

    def load(self, path):
        # """!
        # @brief Calculates the overlapped width between the two both projectors

        # @param w Width of the projected image from one projector [cm]
        # @param d Distance between the two projectors [cm]
        # @return Width of the overlapping screen regions [cm]
        # @rtype float

        # """
        """!
                @brief Reads the settings file (settings.json) and fills in all attributes. A missing file or setting should give an error that names the problem
        
                @param path location of the file (string)
                @return nothing
                @rtype None
                """
        # ˅
        pass
        # ˄

    def validate(self):
        """!
                @brief Checks that the loaded settings are usable. The exact checks are being finalised, for example positive numbers and an existing source file. Call it after load() and before using any setting

                @return nothing
                @rtype None
                """
        # ˅
        pass
        # ˄

    def getProjectorResXY(self):
        # ˅
        pass
        # ˄

    def getImageWidthCm(self):
        # ˅
        pass
        # ˄

    def getProjectorSpacingCm(self):
        # ˅
        pass
        # ˄

    def getBlendCurveGamma(self):
        # ˅
        pass
        # ˄

    def getSourcePath(self):
        # ˅
        pass
        # ˄

    def getProjectorSide(self):
        # ˅
        pass
        # ˄

    def __init__(self):

        self.__projectorResXY = None

        self.__imageWidthCm = None

        self.__projectorSpacingCm = None

        self.__blendCurveGamma = None

        self.__sourcePath = None

        self.__projectorSide = None

        # ˅
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
