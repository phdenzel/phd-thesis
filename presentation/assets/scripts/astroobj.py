#!/usr/bin/env python3
"""
Animation objects for astronomical bodies
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anima
from animobj import AnimObj


class AstroObj(AnimObj):
    """
    Base class for all astro animations
    """
    def __init__(self, suffix, **kwargs):
        AstroObj.parse_config(self, kwargs)
        if isinstance(suffix, int):
            suffix = str(suffix)
        basename = "".join([self.basename, str(suffix)])
        AnimObj.__init__(self, basename, **kwargs)


class Photon(AstroObj):
    CONFIG = dict(
        basename="arrowp",
        stypes=[str(nmbr) for nmbr in range(1, 10)],
    )


class Earth(AstroObj):
    CONFIG = dict(
        flip=False,
        basename="earth",
        stypes=[""]
    )


class Star(AstroObj):
    CONFIG = dict(
        flip=False,
        basename="star",
        stypes=[str(nmbr) for nmbr in range(1, 8)],
    )


class StarCluster(AstroObj):
    CONFIG = dict(
        flip=False,
        basename="scluster",
        stypes=[str(nmbr) for nmbr in range(1, 9)],
    )


class Galaxy(AstroObj):
    CONFIG = dict(
        flip=False,
        basename="galaxy",
        stypes=[str(nmbr) for nmbr in range(1, 10)],
    )


class ProtoGalaxy(AstroObj):
    CONFIG = dict(
        flip=False,
        basename="proto_galaxy",
        stypes=[str(nmbr) for nmbr in range(1, 5)],
    )


class CosmicMB(AstroObj):
    CONFIG = dict(
        basename="cmb",
        stypes=[str(nmbr) for nmbr in range(1, 6)],
    )
