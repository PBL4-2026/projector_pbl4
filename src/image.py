#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class Image(object):
    """!
    @brief A picture held in memory. Placeholder class in the skeleton; it will wrap the OpenCV image type
    """
    # ˅
    
    # ˄

    def load(self, path):
        """!
                @brief Reads the file at path as a colour picture and keeps it inside the object.

                @param path location of the picture (string)
                @return the frame (NumPy array)
                @rtype numpy.ndarray
                """
        # ˅
        pass
        # ˄

    def getFrame(self):
        """!
                @brief Gives the picture data.

                @param none
                @return the frame, or None if nothing is loaded
                @rtype numpy.ndarray
                """
        # ˅
        pass
        # ˄

    def getShape(self):
        """!
                @brief Gives the picture size.

                @param none
                @return (height, width, channels)
                @rtype tuple
                """
        # ˅
        pass
        # ˄

    def setFrame(self, frame):
        """!
                @brief Puts new picture data into the object. Used for the results of scaling, cropping and masking.

                @param frame the new picture data (NumPy array)
                @return nothing
                @rtype None
                """
        # ˅
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
