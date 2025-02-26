import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import griddata
from matplotlib.path import Path
from matplotlib.patches import PathPatch



def strain2d(eb, es, xbi, ybi, xsj, ysj, asj, ci):
    """Относительные деформации в железобетонном сечении."""

    xc = xbi
    yc = ybi
    zc = eb
    epsmin = min(zc)
    epsmax = max(zc)
    x_min = np.array(xc[zc == epsmin][:1])[0]
    y_min = np.array(yc[zc == epsmin][:1])[0]
    x_max = np.array(xc[zc == epsmax][:1])[0]
    y_max = np.array(yc[zc == epsmax][:1])[0]
    x1 = np.linspace(xc.min(), xc.max(), len(xc))
    y1 = np.linspace(yc.min(), yc.max(), len(yc))
    x2, y2 = np.meshgrid(x1, y1)
    z2 = griddata((xc, yc), zc, (x1[None, :], y1[:, None]), method='linear')
    clipindex = ci
    fig, ax = plt.subplots(num=strain2d.__doc__)
    ax.set_xlabel('X, м')
    ax.set_ylabel('Y, м')
    ax.set_aspect('equal')
    plt.subplots_adjust(left=0.185, right=0.815, bottom=0.1, top=0.9)
    plt.title(strain2d.__doc__, pad=20)
    cont = ax.contourf(x2, y2, z2, 20, alpha=0.6, cmap="rainbow")
    clippath = Path(np.c_[xbi[clipindex], ybi[clipindex]])
    patch = PathPatch(clippath, facecolor='none', edgecolor='k')
    ax.add_patch(patch)
    xr = xsj
    yr = ysj
    zr = es
    a_s = asj
    ds = np.sqrt(4 * a_s / np.pi)
    ax.scatter(xr, yr, s=ds * 8000, c='green', alpha=0.5)
    ax.scatter(x_min, y_min, s=100, c='blue')
    ax.scatter(x_max, y_max, s=100, c='red')
    ax.annotate(round(epsmin, 5), (x_min, y_min), size=10, xytext=(
        0, 10), ha='right', color='blue', textcoords='offset points')
    ax.annotate(round(epsmax, 5), (x_max, y_max), size=10, xytext=(
        0, 10), ha='left', color='red', textcoords='offset points')
    for i, txt in enumerate(zr):
        ax.annotate(round(txt, 5), (xr[i], yr[i]), size=10, xytext=(
            0, 0), ha='center', textcoords='offset points')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='10%', pad=0.75)
    plt.colorbar(cont, cax=cax)
    plt.show()


def stress2d(sb, ss, xbi, ybi, xsj, ysj, asj, ci):
    """Напряжения в железобетонном сечении, МПа."""

    xc = xbi
    yc = ybi
    zc = sb
    stressmin = min(zc)
    stressmax = max(zc)
    x_min = np.array(xc[zc == stressmin][:1])[0]
    y_min = np.array(yc[zc == stressmin][:1])[0]
    x_max = np.array(xc[zc == stressmax][:1])[0]
    y_max = np.array(yc[zc == stressmax][:1])[0]
    x1 = np.linspace(xc.min(), xc.max(), len(xc))
    y1 = np.linspace(yc.min(), yc.max(), len(yc))
    x2, y2 = np.meshgrid(x1, y1)
    z2 = griddata((xc, yc), zc, (x1[None, :], y1[:, None]), method='linear')
    clipindex = ci
    fig, ax = plt.subplots(num=stress2d.__doc__)
    ax.set_xlabel('X, м')
    ax.set_ylabel('Y, м')
    ax.set_aspect('equal')
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    plt.title(stress2d.__doc__, pad=20)
    cont = ax.contourf(x2, y2, z2, 20, alpha=0.6, cmap="rainbow")
    clippath = Path(np.c_[xbi[clipindex], ybi[clipindex]])
    patch = PathPatch(clippath, facecolor='none', edgecolor='k')
    ax.add_patch(patch)
    xr = xsj
    yr = ysj
    zr = ss
    a_s = asj
    ds = np.sqrt(4 * a_s / np.pi)
    ax.scatter(xr, yr, s=ds * 8000, c='green', alpha=0.5)
    ax.scatter(x_min, y_min, s=100, c='blue')
    ax.scatter(x_max, y_max, s=100, c='red')
    ax.annotate(round(stressmin, 2), (x_min, y_min), size=10, xytext=(
        0, 10), ha='right', color='blue', textcoords='offset points')
    ax.annotate(round(stressmax, 2), (x_max, y_max), size=10, xytext=(
        0, 10), ha='left', color='red', textcoords='offset points')
    for i, txt in enumerate(zr):
        ax.annotate(round(txt, 2), (xr[i], yr[i]), size=10, xytext=(
            0, 0), ha='center', textcoords='offset points')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='10%', pad=0.75)
    plt.colorbar(cont, cax=cax)
    plt.show()


def strain3d(eb, xbi, ybi):
    """Относительные деформации в железобетонном сечении."""

    xc = xbi
    yc = ybi
    zc = eb
    x1 = np.linspace(xc.min(), xc.max(), len(xc))
    y1 = np.linspace(yc.min(), yc.max(), len(yc))
    x2, y2 = np.meshgrid(x1, y1)
    fig = plt.figure(num=strain3d.__doc__)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    ax = plt.axes(projection='3d')
    ax.set_aspect('auto')
    ax.set_xlabel('X, м')
    ax.set_ylabel('Y, м')
    ax.set_zlabel(zlabel='Относительные деформации')
    z2 = griddata((xc, yc), zc, (x2, y2), method='linear')
    surf = ax.plot_surface(x2, y2, z2, cmap="rainbow", alpha=0.8, linewidth=1)
    plt.title(strain3d.__doc__, pad=10)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, orientation='vertical', shrink=0.5, aspect=5, pad=0.1)
    plt.show()


def stress3d(sb, xbi, ybi):
    """Напряжения в железобетонном сечении, МПа."""

    xc = xbi
    yc = ybi
    zc = sb
    x1 = np.linspace(xc.min(), xc.max(), len(xc))
    y1 = np.linspace(yc.min(), yc.max(), len(yc))
    x2, y2 = np.meshgrid(x1, y1)
    fig = plt.figure(num=stress3d.__doc__)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    ax = plt.axes(projection='3d')
    ax.set_aspect('auto')
    ax.set_xlabel('X, м')
    ax.set_ylabel('Y, м')
    ax.set_zlabel(zlabel='Напряжения, МПа')
    z2 = griddata((xc, yc), zc, (x2, y2), method='linear')
    surf = ax.plot_surface(x2, y2, z2, cmap="rainbow", alpha=0.8, linewidth=1)
    plt.title(stress3d.__doc__, pad=10)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, orientation='vertical', shrink=0.5, aspect=5, pad=0.1)
    plt.show()
