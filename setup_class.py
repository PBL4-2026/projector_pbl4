#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
import json
import logging
import math
import os

from side import Side

_log = logging.getLogger(__name__)

_KEY_RES = "projectorResXY"
_KEY_WIDTH = "imageWidthCm"
_KEY_SPACING = "projectorSpacingCm"
_KEY_GAMMA = "blendCurveGamma"
_GAMMA_MIN = 0.5   # placeholder, not decided
_GAMMA_MAX = 3.0   # placeholder, not decided
_KEY_SOURCE = "sourcePath"
_KEY_SIDE = "projectorSide"
# ˄


class SetupClass(object):
    # ˅
    
    # ˄

    def load(self, path):
        # ˅
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Settings file not found: '%s'" % path)
        except json.JSONDecodeError as e:
            raise ValueError("Settings file '%s' is not valid JSON: %s" % (path, e))

        if not isinstance(data, dict):
            raise ValueError("Settings file '%s' must contain a JSON object at the top level" % path)

        for key in (_KEY_RES, _KEY_WIDTH, _KEY_SPACING, _KEY_GAMMA, _KEY_SOURCE, _KEY_SIDE):
            if key not in data:
                raise ValueError("Missing setting '%s' in '%s'" % (key, path))

        res = self.__toResolution(data[_KEY_RES])
        width = self.__toFloat(_KEY_WIDTH, data[_KEY_WIDTH])
        spacing = self.__toFloat(_KEY_SPACING, data[_KEY_SPACING])
        gamma = self.__toFloat(_KEY_GAMMA, data[_KEY_GAMMA])
        source = data[_KEY_SOURCE]
        if not isinstance(source, str) or not source.strip():
            raise ValueError("Setting '%s' must be a non-empty string (file path), got %r" % (_KEY_SOURCE, source))
        source = os.path.expanduser(source)
        if not os.path.isabs(source):
            source = os.path.join(os.path.dirname(os.path.abspath(path)), source)
        side = self.__toSide(data[_KEY_SIDE])

        self.__projectorResXY = res
        self.__imageWidthCm = width
        self.__projectorSpacingCm = spacing
        self.__blendCurveGamma = gamma
        self.__sourcePath = source
        self.__projectorSide = side
        # ˄

    def validate(self):
        # ˅
        res = self.__projectorResXY
        if (not isinstance(res, list) or len(res) != 2
                or not all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in res)):
            return self.__fail("%s must be two positive integers [width, height] in px, got %r" % (_KEY_RES, res))

        w = self.__imageWidthCm
        if not self.__isPositiveNumber(w):
            return self.__fail("%s must be a positive number (cm), got %r" % (_KEY_WIDTH, w))

        d = self.__projectorSpacingCm
        if not self.__isPositiveNumber(d):
            return self.__fail("%s must be a positive number (cm), got %r" % (_KEY_SPACING, d))

        if d >= w:
            return self.__fail("%s (%s cm) must be smaller than %s (%s cm), otherwise the projectors do not overlap"
                               % (_KEY_SPACING, d, _KEY_WIDTH, w))

        g = self.__blendCurveGamma
        if not self.__isPositiveNumber(g) or not (_GAMMA_MIN <= g <= _GAMMA_MAX):
            return self.__fail("%s must be between %s and %s, got %r" % (_KEY_GAMMA, _GAMMA_MIN, _GAMMA_MAX, g))
        
        src = self.__sourcePath
        if not isinstance(src, str) or not src.strip():
            return self.__fail("%s must be a non-empty path, got %r" % (_KEY_SOURCE, src))
        if not os.path.isfile(src):
            return self.__fail("Source image not found: '%s'" % src)

        if not isinstance(self.__projectorSide, Side):
            return self.__fail("%s must be LEFT or RIGHT, got %r" % (_KEY_SIDE, self.__projectorSide))

        return True
        # ˄

    def getProjectorResXY(self):
        # ˅
        return list(self.__projectorResXY) if self.__projectorResXY is not None else None
        # ˄

    def getImageWidthCm(self):
        # ˅
        return self.__imageWidthCm
        # ˄

    def getProjectorSpacingCm(self):
        # ˅
        return self.__projectorSpacingCm
        # ˄

    def getBlendCurveGamma(self):
        # ˅
        return self.__blendCurveGamma
        # ˄

    def getSourcePath(self):
        # ˅
        return self.__sourcePath
        # ˄

    def getProjectorSide(self):
        # ˅
        return self.__projectorSide
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

    @staticmethod
    def __isPositiveNumber(value):
        return (isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value) and value > 0)

    @staticmethod
    def __fail(message):
        _log.error("Invalid settings: %s", message)
        return False

    @staticmethod
    def __toFloat(name, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Setting '%s' must be a number, got %r" % (name, value))
        return float(value)

    @staticmethod
    def __toResolution(value):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("Setting '%s' must be a list of two integers [width, height], got %r"
                             % (_KEY_RES, value))
        out = []
        for v in value:
            if isinstance(v, bool) or not isinstance(v, int):
                raise ValueError("Setting '%s' must contain integers, got %r" % (_KEY_RES, value))
            out.append(v)
        return out

    @staticmethod
    def __toSide(value):
        if isinstance(value, str) and value.strip().upper() in Side.__members__:
            return Side[value.strip().upper()]
        if isinstance(value, int) and not isinstance(value, bool):
            try:
                return Side(value)
            except ValueError:
                pass
        raise ValueError("Setting '%s' must be LEFT or RIGHT (or 1 / 2), got %r" % (_KEY_SIDE, value))

    def setProjectorSide(self, side):
        """Override projectorSide after load(), so both computers can share one settings file.

        side: Side.LEFT or Side.RIGHT. Raises ValueError for anything else.
        """
        if not isinstance(side, Side):
            raise ValueError("side must be a Side, got %r" % (side,))
        self.__projectorSide = side
    # ˄


# ˅

# ˄
