#!/usr/bin/env python3
"""
Animation scenes for presentations
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anima
from animobj import AnimObj
from astroobj import Photon


def turn_on():
    global objs, imgs

    ax = plt.gca()

    lamp = AnimObj('scenes/lamp1', scale=1.5)
    limg = ax.imshow(lamp.pixel_array, extent=lamp.extent)

    centimeter = AnimObj('scenes/cm30', position=L/2 - 1j*L/6, scale=2., flip=False)
    centimeter.phase_io(-0.99)
    cimg = ax.imshow(centimeter.pixel_array, extent=centimeter.extent)

    nanosec = AnimObj('scenes/nanosec1', position=L/2 + 1j*L/6, scale=2., flip=False)
    nanosec.phase_io(-0.99)
    nimg = ax.imshow(nanosec.pixel_array, extent=nanosec.extent)

    objs = [lamp, centimeter, nanosec]
    imgs = [limg, cimg, nimg]


def lamplight(i, dx, zoom):

    ax = plt.gca()

    for p in objs:
        p.increment()

    if N_photons > len(photons) and (i == 50 or i == 100 or i == 150):
        # stypes = Photon.CONFIG['stypes']
        # stype = stypes[np.random.randint(len(stypes))]
        photon = Photon(suffix="9", position=0.5+0j, rotation=180, scale=pscale)
        photon.phase_io(-0.99)
        photons.append(photon)
        pimg = ax.imshow(photon.pixel_array, extent=photon.extent)
        pimgs.append(pimg)

    for p, photon in enumerate(photons):
        pimg = pimgs[p]

        # move
        photon.move(dx, radial=True, increment=True)
        pimg.set_data(photon.pixel_array)
        pimg.set_extent(photon.extent)

        # reset
        if photon.distance > L:
            photon.reset(0.5+0j, phase_io=-0.99, scale=pscale, rotation=180)

        # phase in and out
        inc = 0.02
        phasein = int(0.5/inc)
        if photon.steps < phasein:
            photon.phase_shift(inc)

    # fade-in
    if objs[1].steps > 50:
        objs[1].phase_shift(inc)
        imgs[1].set_data(objs[1].pixel_array)
    if objs[2].steps > 100:
        objs[2].phase_shift(inc)
        imgs[2].set_data(objs[2].pixel_array)


def lamp_scene():

    global L, offset, nframes, verbose
    verbose = True
    aspect = (16, 9)
    fps = 60                  # Hz
    duration = 4              # s
    nframes = duration * fps  # 240
    dt = 1000/fps             # ms
    L = 5                     # length units
    offset = 1                # length units
    dx = 2*L/nframes        # length units

    global photons, pimgs, N_photons, pscale
    N_photons = 1
    photons = []
    pimgs = []
    pscale = 1.
    global objs, imgs
    objs = []
    imgs = []

    global N1, N2, M1, M2
    zoom = 1
    plt.style.use('dark_background')
    fig = plt.figure(figsize=aspect)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    N1, N2 = -L/6, L*5/6
    M1, M2 = -0.5*L/np.divide(*aspect), 0.5*L/np.divide(*aspect)
    ax.set_xlim(N1*zoom, N2*zoom)
    ax.set_ylim(M1*zoom, M2*zoom)
    ax.set_axis_off()

    nframes = int(3*nframes)
    a = anima.FuncAnimation(
        fig, lamplight, init_func=turn_on, fargs=(-dx, zoom),
        frames=nframes, interval=dt
    )
    savename = 'lamp_u'
    ext = 'mp4'
    a.save("{}.{}".format(savename, ext), fps=fps)


###############################################################################
def fuse():
    global objs, imgs

    ax = plt.gca()

    sun = AnimObj('scenes/sun', position=-4/6*L+0.7j, scale=1.5)
    simg = ax.imshow(sun.pixel_array, extent=sun.extent)

    earth = AnimObj('earth', position=-0.2j, scale=0.5, flip=False)
    eimg = ax.imshow(earth.pixel_array, extent=earth.extent)

    objs = [sun, earth]
    imgs = [simg, eimg]


def sunlight(i, dx, zoom):
    ax = plt.gca()

    for p in objs:
        p.increment()

    if N_photons > len(photons):
        photon = Photon(suffix="9", position=objs[0].position, scale=pscale)
        theta = np.arctan2(objs[0].position.imag, objs[0].position.real)/AnimObj.DEG2RAD
        photon.rotate(theta, inplace=True)
        photon.phase_io(-0.99)
        photons.append(photon)
        pimg = ax.imshow(photon.pixel_array, extent=photon.extent)
        pimgs.append(pimg)

    for p, photon in enumerate(photons):
        pimg = pimgs[p]

        # move
        photon.move(dx, radial=True, increment=True)
        pimg.set_data(photon.pixel_array)
        pimg.set_extent(photon.extent)

        # reset
        if photon.distance <= 0:
            photon.reset(objs[0].position, phase_io=-0.99, scale=pscale, rotation=0)

        # phase in and out
        inc = 0.05
        phasein = int(0.5/inc)
        if photon.steps < phasein:
            photon.phase_shift(inc)
        if photon.distance <= offset:
            photon.phase_shift(-inc)


def sun_scene():
    global L, offset, nframes, verbose
    verbose = True
    aspect = (16, 10)
    fps = 60                  # Hz
    duration = 4              # s
    nframes = duration * fps  # 240
    dt = 1000/fps             # ms
    L = 5                     # length units
    offset = 1                # length units
    dx = 2*L/nframes          # length units

    global photons, pimgs, N_photons, pscale
    N_photons = 1
    photons = []
    pimgs = []
    pscale = 0.5
    global objs, imgs
    objs = []
    imgs = []

    global N1, N2, M1, M2
    zoom = 1
    plt.style.use('dark_background')
    fig = plt.figure(figsize=aspect)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    N1, N2 = -L*5/6, L*1/6
    M1, M2 = -0.5*L/np.divide(*aspect), 0.5*L/np.divide(*aspect)
    ax.set_xlim(N1*zoom, N2*zoom)
    ax.set_ylim(M1*zoom, M2*zoom)
    ax.set_axis_off()

    nframes = int(0.95*nframes)
    a = anima.FuncAnimation(
        fig, sunlight, init_func=fuse, fargs=(dx, zoom),
        frames=nframes, interval=dt
    )
    savename = 'sun_u'
    ext = 'mp4'
    a.save("{}.{}".format(savename, ext), fps=fps)


###############################################################################
def alphac():
    global objs, imgs

    ax = plt.gca()
    centauri = AnimObj('scenes/alphacentauri', position=0.3-0.4j, scale=4, flip=False)
    cimg = ax.imshow(centauri.pixel_array, extent=centauri.extent)

    objs = [centauri]
    imgs = [cimg]
    ax.set_xlim(centauri.extent[0], centauri.extent[1])
    ax.set_ylim(centauri.extent[2], centauri.extent[3])


def starlight(i, dx):
    ax = plt.gca()

    for p in objs:
        p.increment()

    pos = 1.75+0.28j
    if N_photons > len(photons):
        photon = Photon(suffix="9", position=pos, scale=pscale)
        theta = np.arctan2(pos.imag, pos.real)/AnimObj.DEG2RAD
        photon.rotate(theta, inplace=True)
        photon.phase_io(-0.99)
        photons.append(photon)
        pimg = ax.imshow(photon.pixel_array, extent=photon.extent)
        pimgs.append(pimg)

    for p, photon in enumerate(photons):
        pimg = pimgs[p]

        # move
        photon.move(dx, radial=True, increment=True)
        pimg.set_data(photon.pixel_array)
        pimg.set_extent(photon.extent)

        # reset
        if photon.distance <= 0:
            photon.reset(pos, phase_io=-0.99, scale=pscale, rotation=0)

        # phase in and out
        inc = 0.05
        phasein = int(0.5/inc)
        if photon.steps < phasein:
            photon.phase_shift(inc)
        if photon.distance <= offset:
            photon.phase_shift(-inc)


def centauri_scene():
    global offset, nframes, verbose
    verbose = True
    aspect = (16, 10)
    fps = 60                  # Hz
    duration = 4              # s
    nframes = duration * fps  # 240
    dt = 1000/fps             # ms
    offset = 0.4              # length units
    dx = 0.02                 # length units

    global photons, pimgs, N_photons, pscale
    N_photons = 1
    photons = []
    pimgs = []
    pscale = 0.5
    global objs, imgs
    objs = []
    imgs = []

    plt.style.use('dark_background')
    fig = plt.figure(figsize=aspect)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.set_axis_off()

    nframes = int(0.5*nframes)
    a = anima.FuncAnimation(
        fig, starlight, init_func=alphac, fargs=(dx,),
        frames=nframes+3, interval=dt
    )
    savename = 'alpha_centauri_u'
    ext = 'mp4'
    a.save("{}.{}".format(savename, ext), fps=fps)


###############################################################################
def peerout():
    global objs, imgs

    ax = plt.gca()
    andromeda = AnimObj('scenes/andromeda', position=0.5+0.1j, scale=4, flip=False)
    aimg = ax.imshow(andromeda.pixel_array, extent=andromeda.extent)

    objs = [andromeda]
    imgs = [aimg]
    ax.set_xlim(andromeda.extent[0], andromeda.extent[1])
    ax.set_ylim(andromeda.extent[2], andromeda.extent[3])


def galaxylight(i, dx):
    ax = plt.gca()

    for p in objs:
        p.increment()

    pos = 1.75+0.6j
    if N_photons > len(photons):
        photon = Photon(suffix="9", position=pos, scale=pscale)
        theta = np.arctan2(pos.imag, pos.real)/AnimObj.DEG2RAD
        photon.rotate(theta, inplace=True)
        photon.phase_io(-0.99)
        photons.append(photon)
        pimg = ax.imshow(photon.pixel_array, extent=photon.extent)
        pimgs.append(pimg)

    for p, photon in enumerate(photons):
        pimg = pimgs[p]

        # move
        photon.move(dx, radial=True, increment=True)
        pimg.set_data(photon.pixel_array)
        pimg.set_extent(photon.extent)

        # reset
        if photon.distance <= 0:
            photon.reset(pos, phase_io=-0.99, scale=pscale, rotation=0)

        # phase in and out
        inc = 0.05
        phasein = int(0.5/inc)
        if photon.steps < phasein:
            photon.phase_shift(inc)
        if photon.distance <= offset:
            photon.phase_shift(-inc)


def andromeda_scene():
    global offset, nframes, verbose
    verbose = True
    aspect = (16, 10)
    fps = 60                  # Hz
    duration = 4              # s
    nframes = duration * fps  # 240
    dt = 1000/fps             # ms
    offset = 0.4              # length units
    dx = 0.02                 # length units

    global photons, pimgs, N_photons, pscale
    N_photons = 1
    photons = []
    pimgs = []
    pscale = 0.5
    global objs, imgs
    objs = []
    imgs = []

    plt.style.use('dark_background')
    fig = plt.figure(figsize=aspect)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.set_axis_off()

    nframes = int(0.5*nframes)
    a = anima.FuncAnimation(
        fig, galaxylight, init_func=peerout, fargs=(dx,),
        frames=nframes+7, interval=dt
    )
    savename = 'andromeda_u'
    ext = 'mp4'
    a.save("{}.{}".format(savename, ext), fps=fps)


if __name__ == "__main__":

    # lamp_scene()

    # sun_scene()

    # centauri_scene()

    andromeda_scene()
