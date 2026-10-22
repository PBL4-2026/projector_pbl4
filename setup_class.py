#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class SetupClass(object):
     """!
    @brief SetupClass reads settings.json, including which side this computer shows, then validate() checks it.

    
    SetupClass stores and checks the user's settings. It does no calculations. 
    Its attributes are private (a double underscore in Python) and are read through the getters.

    """
    # ˅
    
    # ˄

    def load(self, path):
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
        """!
                @brief Gives the projector resolution

                @param none
                @return List of two integers [px]
                @rtype list
                """
        # ˅
        pass
        # ˄

    def getImageWidthCm(self):
        """!
                @brief Gives the width of the projected image from one projector [cm]

                @param none
                @return float [cm]
                @rtype float
                """
        # ˅
        pass
        # ˄

    def getProjectorSpacingCm(self):
        """!
                @brief Gives the spacing between the projectors [cm]

                @param none
                @return float [cm]
                @rtype float
                """
        # ˅
        pass
        # ˄

    def getBlendCurveGamma(self):
        """!
                @brief Gives the gamma value for the blend curve

                @param none
                @return float
                @rtype float
                """
        # ˅
        pass
        # ˄

    def getSourcePath(self):
        """!
                @brief Gives the path of the image to display

                @param none
                @return string
                @rtype string
                """
        # ˅
        pass
        # ˄

    def getProjectorSide(self):
        """!
                @brief Gives which projector this computer drives

                @param none
                @return Side
                @rtype Side
                """
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
