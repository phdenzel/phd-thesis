#!/usr/bin/env python3
"""
Animation scenes for presentations
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anima
from animobj import AnimObj
from astroobj import Photon
from astroobj import Earth
from astroobj import Star
from astroobj import StarCluster
from astroobj import Galaxy
from astroobj import ProtoGalaxy
from astroobj import CosmicMB


def bigbang():
    """
    Create the Universe
    """
    if verbose:
        print("Populate...")
    populate()
    if verbose:
        print("Illuminate...")
    shine()
    if verbose:
        print("Steps:\t", end="")


def populate(d_star=0.1,
             d_scluster=0.2,
             d_galaxy=0.4,
             d_proto_galaxy=0.6,
             d_cmb=1.):
    global aobjs, aimgs
    # Me
    o, p = epoch(Earth, 1, align=True, angles=np.array([0]),
                 scale=3., distance=0, spread=0)
    aobjs += o*1
    aimgs += p*1
    # Stars
    o, p = epoch(Star, 6, scale=2., distance=L*d_star, spread=0.05)
    aobjs += o*1
    aimgs += p*1
    # Star clusters
    o, p = epoch(StarCluster, 12, scale=2., distance=L*d_scluster, spread=0.05)
    aobjs += o*1
    aimgs += p*1
    # Galaxies
    o, p = epoch(Galaxy, 24, scale=5., distance=L*d_galaxy, spread=0.05)
    aobjs += o*1
    aimgs += p*1
    # Proto-Galaxies
    o, p = epoch(ProtoGalaxy, 12, scale=5., distance=L*d_proto_galaxy, spread=0.05)
    aobjs += o*1
    aimgs += p*1
    # CMB
    orientation = np.linspace(0, 2*np.pi, 36)
    o, p = epoch(CosmicMB, 36, scale=12., align=True,
                 angles=orientation,
                 distance=L*d_cmb, spread=0.0)
    aobjs += o*1
    aimgs += p*1


def shine():
    global photons, pimgs
    distance = 3*L/4.
    spread = L/4.
    photons, pimgs = epoch(Photon, N_photons, scale=pscale,
                           distance=distance, spread=spread,
                           align=True, fade_in=True)


def epoch(cls, N_obj, distance=1., spread=0.25, angles=None,
          scale=1., align=False, fade_in=False):
    """
    Create a cosmic epoch
    """
    objs = []
    imgs = []
    ax = plt.gca()
    rand_r = np.random.normal(distance, spread, N_obj)
    if angles is not None:
        rand_t = angles
    else:
        rand_t = np.random.uniform(0, 2*np.pi, N_obj)
    rand_pos = rand_r * np.e**(1j*rand_t)
    for p in range(N_obj):
        if cls.__name__ == "CosmicMB":
            stypes = [2, 3, 4, 5, 5, 4, 4, 5, 4, 3, 5, 2, 3, 3, 2, 3, 4, 5,
                      3, 5, 3, 3, 5, 2, 3, 3, 3, 5, 5, 4, 5, 3, 5, 3, 2, 2]
            stype = stypes[p]
        else:
            stypes = cls.CONFIG['stypes']
            stype = stypes[np.random.randint(len(stypes))]
        obj = cls(suffix=stype, position=rand_pos[p])
        obj.scale = scale
        if fade_in:
            obj.phase_io(-0.99)
        if align:
            # theta = rand_t[p]/AnimObj.DEG2RAD
            # if cls.__name__ == "CosmicMB":
            #     if (10 < theta < 80) or (190 < theta < 260):
            #         theta -= 10
            #     elif (100 < theta < 170) or (280 < theta < 350):
            #         theta += 2
            obj.rotate(rand_t[p]/AnimObj.DEG2RAD, inplace=True)
        else:
            obj.rotate(np.random.uniform(0, 360), inplace=True)
        img = ax.imshow(obj.pixel_array, extent=obj.extent)
        objs.append(obj)
        imgs.append(img)
    return objs, imgs


def dynamics(i, dx, zoom):

    if verbose:
        print(i, end=", ")

    # Photon propagation
    for p in range(N_photons):
        photon = photons[p]
        pimg = pimgs[p]

        # move
        photon.move(dx, radial=True, increment=True)
        pimg.set_data(photon.pixel_array)
        pimg.set_extent(photon.extent)

        # detection
        if photon.distance == 0:
            rand_r = np.random.normal(L, L/5.)
            rand_t = np.random.uniform(0, 2*np.pi)
            pos = rand_r * np.e**(1j*rand_t)
            photon.reset(pos, phase_io=-0.99, scale=pscale)

        # phase in and out
        inc = 0.01
        phasein = int(0.5/inc)
        if photon.steps < phasein:
            photon.phase_shift(inc)
        if photon.distance <= offset:
            photon.phase_shift(-inc)
            photon.rescale(1-inc)

    # zoom out
    ax = plt.gca()
    zoom = min(1, zoom + 0.001*i)
    ax.set_xlim(N1*zoom, N2*zoom)
    ax.set_ylim(M1*zoom, M2*zoom)
    for p in photons:
        p.scale = pscale * 2*zoom/(1+zoom**2)

    # fade out
    if (nframes - i) < 100:
        for p in photons:
            p.phase_shift(-0.02)


def universe_scene(*args):

    global L, offset, nframes, verbose
    verbose = True
    aspect = (16, 10)
    fps = 60                  # Hz
    duration = 4              # s
    nframes = duration * fps  # 240
    dt = 1000/fps             # ms
    L = 25                    # length units
    offset = 5               # length units
    dx = 0.5*L/nframes        # length units

    global photons, pimgs, N_photons, pscale
    N_photons = 75
    photons = []
    pimgs = []
    pscale = 3.
    global aobjs, aimgs
    aobjs = []
    aimgs = []

    global N1, N2, M1, M2
    zoom = 0.1
    plt.style.use('dark_background')
    fig = plt.figure(figsize=aspect)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    N1, N2 = -L-3, L+3
    M1, M2 = N1/np.divide(*aspect), N2/np.divide(*aspect)
    ax.set_xlim(N1*zoom, N2*zoom)
    ax.set_ylim(M1*zoom, M2*zoom)
    ax.set_axis_off()

    nframes = int(6 * nframes)
    a = anima.FuncAnimation(
        fig, dynamics, init_func=bigbang, fargs=(dx, zoom),
        frames=nframes, interval=dt, repeat=False)
    savename = 'dyna_u'
    ext = 'mp4'  # 'gif'
    a.save("{}.{}".format(savename, ext), fps=fps)


if __name__ == "__main__":

    universe_scene()
