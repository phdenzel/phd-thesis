#!/usr/bin/env python3
"""
Animate the propagation of light for presentations
"""
import os
import itertools as it
import numpy as np
from scipy import ndimage
from PIL import Image
import cv2
# import manimlib
# check out
# https://talkingphysics.wordpress.com/2019/01/08/getting-started-animating-with-manim-and-python-3-7/
# also check out
# https://github.com/3b1b/manim/blob/master/manimlib/mobject/mobject.py
# https://github.com/3b1b/manim/blob/master/manimlib/mobject/types/image_mobject.py


def compile_config(obj, kwargs, caller_locals={}):
    """
    Sets a class' init args and CONFIG values as local variables

    Args:
        obj <instance> - class instance
        kwargs <dict> - keywords directly passed to the class' __init__

    Kwargs:
        caller_locals <dict> - additional locals to set

    Return:
        None
    """
    classes_in_hierarchy = [obj.__class__]
    static_configs = []
    while len(classes_in_hierarchy) > 0:
        cls = classes_in_hierarchy.pop()
        classes_in_hierarchy += cls.__bases__
        if hasattr(cls, "CONFIG"):
            static_configs.append(cls.CONFIG)
    # sanitize
    locs = caller_locals.copy()
    for arg in ["self", "kwargs"]:
        locs.pop(arg, caller_locals)
    all_dcts = [kwargs, locs, obj.__dict__]
    all_dcts += static_configs
    obj.__dict__ = recurse_merge(*reversed(all_dcts))


def recurse_merge(*dicts):
    """
    Recursive merge of dictionaries
    Entries of later dictionaries override earier ones

    Args:
        <*dicts> - iteration of dictionaries to merge

    Kwargs:
        None

    Return:
        <dict> - single, fully merged dictionary
    """
    dct = dict()
    all_items = it.chain(*[d.items() for d in dicts])
    for key, val in all_items:
        if key in dct and isinstance(dct[key], dict) and isinstance(val, dict):
            dct[key] = recurse_merge(dct[key], val)
        else:
            dct[key] = val
    return dct


class AnimObj(object):
    CONFIG = dict(
        image_mode="RGBA",
        size=1.,
        scale=1.,
        flip=True,
        alignment=0.,
    )

    DEG2RAD = np.pi/180
    SQRT2 = np.sqrt(2)

    def __init__(self, basename, ext=".png", imgdir="imgs/",
                 position=0j, rotation=0,
                 **kwargs):
        """
        Args:
            basename <str> - name of an image object

        Kwargs:
            ext <str> -
            imgdir <str> -
            position <tuple/tuple|list|np.ndarray> - position of the image
            rotate
            kwargs
        """
        AnimObj.parse_config(self, kwargs)
        self.filename = os.path.join(imgdir, basename+ext)
        self.steps = 0
        self.position = position
        if isinstance(position, complex):
            self.position = position
        elif isinstance(position, (tuple, list, np.ndarray)):
            self.position = position[0] + 1j*position[1]
        image = Image.open(self.filename).convert(self.image_mode)
        self.pixel_array = np.array(image)
        if self.flip:
            self.pixel_array = np.fliplr(self.pixel_array)
        self.image = image
        if rotation > 0:
            self.rotate(rotation)

    @staticmethod
    def parse_config(obj, kwargs, caller_locals={}):
        """
        Wrapper for `compile_config`
        """
        compile_config(obj, kwargs, caller_locals=caller_locals)

    def reset(self, position, phase_io=None, scale=1., rotation=0):
        """
        Reset the photon
        """
        self.steps = 0
        self.alignment = 0
        self.scale = scale
        self.pixel_array = np.array(self.image)
        if self.flip:
            self.pixel_array = np.fliplr(self.pixel_array)
        if isinstance(position, complex):
            self.position = position
            theta = np.arctan2(self.position.imag, self.position.real) \
                / AnimObj.DEG2RAD
        elif isinstance(position, (int, float)):
            self.position = position + 0j
            theta = 0
        elif isinstance(position, (tuple, list, np.ndarray)):
            self.position = position[0] + position[1]*1j
            theta = np.arctan2(self.position.imag, self.position.real) \
                / AnimObj.DEG2RAD
        if theta != 0:
            self.rotate(theta, inplace=True)
        if phase_io:
            self.phase_io(phase_io)
        if rotation > 0:
            self.rotate(rotation)

    def increment(self):
        self.steps += 1

    @property
    def aspect(self):
        h, w, _ = self.pixel_array.shape
        return h / w

    @property
    def extent(self):
        x, y = self.position.real, self.position.imag
        w2 = 0.5 * self.size * self.scale
        h2 = 0.5 * self.size * self.scale * self.aspect
        l, r, b, t = x-w2, x+w2, y-h2, y+h2
        xtnt = [l, r, b, t]
        return xtnt

    @property
    def bounding_radius(self):
        l, r, b, t = self.extent
        dim = abs(l-r)**2 + abs(b-t)**2
        return np.sqrt(dim)/2

    @property
    def distance(self):
        return abs(self.position)

    def move(self, delta, radial=False, limit=0, increment=True):
        """
        Move the center position of objects

        Args:
            delta <int|float/complex/tuple|list|np.ndarray> - translation added to position

        Kwargs:
            radial <bool> - radially move the position to the center
        """
        if radial:
            if isinstance(delta, (int, float)):
                r = abs(self.position) - delta*AnimObj.SQRT2
                theta = np.arctan2(self.position.imag, self.position.real)
                r = max(r, limit)
                self.position = r * np.e**(1j*theta)
            elif isinstance(delta, complex):
                r = abs(self.position + delta)
                theta = np.arctan2(self.position.imag, self.position.real)
                r = max(r, limit)
                self.position = r * np.e**(1j*theta)
            elif isinstance(delta, (tuple, list, np.ndarray)):
                r = abs(self.position + complex(delta[0], delta[1]))
                theta = np.arctan2(self.position.imag, self.position.real)
                r = max(r, limit)
                self.position = r * np.e**(1j*theta)
        else:
            if isinstance(delta, (int, float)):
                self.position += delta + 1j*delta
            elif isinstance(delta, complex):
                self.position += delta
            elif isinstance(delta, (tuple, list, np.ndarray)):
                self.position.real += delta[0]
                self.position.imag += delta[1]
        if increment:
            self.increment()

    def rotate(self, theta, inplace=True):
        """
        """
        self.alignment = (self.alignment + theta) % 360
        self.pixel_array = ndimage.rotate(self.pixel_array, theta, reshape=True)
        if not inplace:
            self.position = self.position * np.e**(1j*theta*AnimObj.DEG2RAD)

    def phase_io(self, ratio):
        """
        Phase objects in or out by alpha channel multiplication

        Args:
            ratio <float> - relative phase ratio
        """
        alpha = self.pixel_array[:, :, 3]
        factor = 1. + ratio
        self.pixel_array[:, :, 3] = cv2.multiply(alpha, factor)

    def phase_shift(self, ratio):
        """
        Phase objects in or out by alpha channel multiplication

        Args:
            ratio <float> - relative phase ratio
        """
        alpha = self.pixel_array[:, :, 3]
        msk = alpha > 0
        if self.pixel_array.dtype == np.uint8:
            shift = np.uint8(max(1, abs(ratio)*255))
        else:
            shift = abs(ratio)
        if ratio > 0:
            self.pixel_array[:, :, 3] = cv2.add(self.pixel_array[:, :, 3], msk*shift)
        else:
            self.pixel_array[:, :, 3] = cv2.subtract(self.pixel_array[:, :, 3], msk*shift)

    def rescale(self, factor):
        """
        Rescale objects by a given factor

        Args:
            factor <float> - scaling factor
        """
        self.scale *= factor
