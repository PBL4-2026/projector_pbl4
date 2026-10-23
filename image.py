#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
import os

import cv2
import numpy as np
# ˄


class Image(object):
    # ˅
    
    # ˄

    def load(self, path):
        # ˅
        """path の画像を BGR（cv2.IMREAD_COLOR）で読み込み、numpy.ndarray として返す。

        path: 画像ファイルのパス
        読み込んだフレームは内部にも保持し、getFrame() / getShape() で参照できる。
        ファイルが存在しない、またはファイルでない場合は FileNotFoundError、
        画像として読み込めない場合は ValueError を送出する。
        """
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"path must be a non-empty string, got {path!r}")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image file not found: '{path}'")
        frame = cv2.imread(path, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError(
                f"Failed to read image '{path}': the file is corrupt "
                "or its format is not supported by OpenCV"
            )
        if not isinstance(frame, np.ndarray):
            raise ValueError(
                f"cv2.imread returned {type(frame).__name__} instead of "
                f"numpy.ndarray for '{path}'"
            )
        self.__frame = frame
        return frame
        # ˄

    def getFrame(self):
        # ˅
        """読み込み済みのフレームを返す。load() をまだ呼んでいなければ None を返す。"""
        return self.__frame
        # ˄

    def getShape(self):
        # ˅
        """読み込み済みのフレームの (height, width, channels) を返す。

        load() をまだ呼んでいない場合は ValueError を送出する。
        """
        if self.__frame is None:
            raise ValueError("No frame is loaded: call load() first")
        return self.__frame.shape
        # ˄

    def __init__(self):

        self.__frame = None

        # ˅
        pass
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
