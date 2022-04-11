import sympy as sp
import matplotlib.pyplot as plt  # needed for graphs
import pathlib  # needed to create folder
import numpy as np
from tqdm import tqdm
import matplotlib.animation as animation


# u_grid[i][j]
# i is time (t)
# j is space (x)


def calc(Dx, fraction_constant):
    u_grid = np.zeros((1000, 1000))
    Dt = fraction_constant * Dx
    for i in range(0, 2):
        for j in range(2, 7):
            u_grid[i][i + j] = 1
        for j in range(7, 12):
            u_grid[i][i + j] = -1

    for i in range(1, 999):
        for j in range(1, 999):
            ctrldfr = (u_grid[i][j + 1] - 2 * u_grid[i][j] + u_grid[i][j - 1]) / Dx**2
            u_grid[i + 1][j] = Dt**2 * ctrldfr + 2 * u_grid[i][j] - u_grid[i - 1][j]
    return u_grid


u_e2_09 = calc(0.01, 0.9)
u_e8_09 = calc(10 ** (-8), 0.9)
u_e2_1 = calc(0.01, 1)
u_e8_1 = calc(10 ** (-8), 1)
u_e2_11 = calc(0.01, 1.1)
u_e8_11 = calc(10 ** (-8), 1.1)
fig, axes = plt.subplots(ncols=1, nrows=3, sharex="col")


def update(i):
    axes[0].clear()
    axes[1].clear()
    axes[2].clear()
    axes[0].set_title(r"$\frac{\Delta t}{\Delta x}=0.9$")
    axes[1].set_title(r"$\frac{\Delta t}{\Delta x}=1$")
    axes[2].set_title(r"$\frac{\Delta t}{\Delta x}=1.1$")
    fig.tight_layout()
    axes[0].plot(u_e2_09[i][:], color="tab:blue")
    axes[1].plot(u_e2_1[i][:], color="tab:green")
    axes[2].plot(u_e2_11[i][:], color="tab:pink")
    plt.draw()


ani = animation.FuncAnimation(fig, update, frames=999)
ani.save(f"hm_all_same_frconst.mp4", dpi=1000, bitrate=-1)
