#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
import math

from mask import Mask
from region import Region
from side import Side


# ˄


class MathClass(object):
    # ˅
    
    # ˄

    @classmethod
    def overlapCm(cls, w, d):
        # ˅
        """2台の投影が重なる幅 o = w - d [cm] を返す。

        w: 1台あたりの投影幅 [cm]
        d: 2台のプロジェクター間隔 [cm]
        w > d の検証は SetupClass.validate() が担当する。
        """
        return float(w) - float(d)
        # ˄

    @classmethod
    def totalWidthCm(cls, w, d):
        # ˅
        """2台を合わせた投影全体の幅 W = w + d [cm] を返す。

        w: 1台あたりの投影幅 [cm]
        d: 2台のプロジェクター間隔 [cm]
        """
        return float(w) + float(d)
        # ˄

    @classmethod
    def pxPerCm(cls, resX, w):
        # ˅
        """投影面 1cm あたりのピクセル数 resX / w [px/cm] を返す。

        resX: プロジェクターの横解像度 [px]
        w: 1台あたりの投影幅 [cm]（0 より大きいこと）
        """
        if w <= 0:
            raise ValueError(f"w must be greater than 0, got {w}")
        return float(resX) / float(w)
        # ˄

    @classmethod
    def overlapPx(cls, resX, w, d):
        # ˅
        # Round half up (not Python round(), which rounds halves to even).
        # This is the only place the overlap is rounded, so both computers agree.
        px = math.floor(cls.overlapCm(w, d) * cls.pxPerCm(resX, w) + 0.5)
        if px < 1 or px >= resX:
            raise ValueError(f"overlapPx must be in [1, resX), got {px} (resX={resX})")
        return int(px)
        # ˄

    @classmethod
    def cropRegion(cls, projectorSide, resX, w, d):
        # ˅
        if not isinstance(projectorSide, Side):
            raise ValueError(f"projectorSide must be a Side, got {projectorSide!r}")
        overlap = cls.overlapPx(resX, w, d)
        if projectorSide is Side.LEFT:
            return Region(0, resX)
        return Region(resX - overlap, resX)
        # ˄

    @classmethod
    def blendMask(cls, overlapPx, resX, projectorSide, gamma):
        # ˅
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
