import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')


def strain(df):
    """Относительные деформации в слоях железобетонной оболочки."""

    plt.figure(num=strain.__doc__)
    ax = plt.gca()
    df.plot(kind='line', x='Z', y='Strain1', color='green', ax=ax)
    df.plot(kind='line', x='Z', y='Strain2', color='red', ax=ax)
    plt.title('Относительные деформации в слоях бетона')
    ax.set_xlabel('Центры слоев бетона оболочки, м')
    ax.set_ylabel('Относительные деформации в слоях бетона')
    plt.subplots_adjust(left=0.185, right=0.815, bottom=0.1, top=0.85)

    plt.show()


def stress(z, df, rstress):
    """Напряжения в слоях железобетонной оболочки, МПа."""

    plt.figure(num=stress.__doc__)
    ax = plt.gca()
    df.plot(kind='line', x='Z', y='Stress1', color='green', ax=ax)
    df.plot(kind='line', x='Z', y='Stress2', color='red', ax=ax)
    ax.scatter(z, np.zeros(len(z)), s=50, c='black', alpha=1.0)
    for i, txt in enumerate(rstress):
        ax.annotate(round(txt, 2), (z[i], 0.0), rotation=90, size=10, xytext=(0, 0), va='top',
                    textcoords='offset points')
    plt.title('Напряжения в слоях бетона и арматуры , МПа')
    ax.set_xlabel('Центры слоев плиты и арматуры, м')
    ax.set_ylabel('Напряжения в слоях бетона и арматуры, МПа')
    plt.subplots_adjust(left=0.185, right=0.815, bottom=0.1, top=0.9)
    plt.show()


def reb3d(plies, rstress, name):
    """3D"""
    i = 0
    fig = plt.figure(num=name)
    ax = fig.add_subplot(111, projection='3d')
    xx, yy = np.meshgrid(np.linspace(-0.5, 0.5, 2), np.linspace(-0.5, 0.5, 2))
    for rbr in plies.keys():
        a = plies[rbr].alpha
        lw = plies[rbr].ds * 100
        x = [-np.cos(a) * 0.5, np.cos(a) * 0.5]
        y = [-np.sin(a) * 0.5, np.sin(a) * 0.5]
        z = [plies[rbr].z, plies[rbr].z]
        ax.plot(x, y, zs=z, linewidth=lw, color='black')
        ax.text(-np.cos(a) * 0.5, -np.sin(a) * 0.5, plies[rbr].z, np.round(rstress[i], 4), size=10, ha='center',
                c='blue')
        zz = np.ones([2, 2]) * plies[rbr].z
        ax.plot_surface(xx, yy, zz, color='grey', alpha=0.2)
        i += 1
    plt.title(name, pad=20)
    ax.set_xlabel('X, м')
    plt.title(name, pad=20)
    ax.set_xlabel('X, м')
    ax.set_ylabel('Y, м')
    ax.set_zlabel('Z, м')
    plt.show()


def con3d(zb, sig1, sig2, orn, name):
    """3D"""
    fig = plt.figure(num=name)
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(zb)):
        s1 = sig1[i][0]
        s2 = sig2[i][0]
        a1 = orn[i]
        a2 = a1 - np.pi / 2
        x = 0
        y = 0
        z = zb[i]
        u1 = np.sin(a1) * np.cos(a1)
        v1 = np.cos(a1) * np.cos(a1)
        u2 = np.sin(a2) * np.cos(a2)
        v2 = np.cos(a2) * np.cos(a2)
        w = zb[i]
        ax.quiver(x, y, z, u1, v1, w, length=s1 / 200, color='green')
        ax.quiver(x, y, z, u2, v2, w, length=s2 / 200, color='red')
    plt.title(name, pad=20)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z, м')
    plt.show()
