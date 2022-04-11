import matplotlib.pyplot as plt  # needed for graphs
import pathlib  # needed to create folder
import numpy as np
from tqdm import tqdm
import matplotlib.animation as animation


def savim(directory: str, name: str) -> None:
    """savim Function to save images to folder

    Args:
        directory (str): Directory path
        name (str): Name of file

    Examples:
    directory = images
    and name = example_image
    saves an image to ./images/example_image.png
    """
    path = pathlib.Path(f"./{directory}")
    path.mkdir(
        exist_ok=True,  # Without exist_ok=True, FileExistsError show up if folder already exists
        parents=True,
    )  # Missing parents of the path are created.
    plt.savefig(f"./{directory}/{name}.png", dpi=dpisiz)
    print(f"Saved image at location: ./{directory}/{name}.png")


dpisiz = 1000


def calc(Dx: float, fraction_constant: float) -> np.ndarray:
    u_grid = np.zeros((1000, 1000))  # u_grid[i][j]
    # i is time (t)
    # j is space (x)
    Dt = fraction_constant * Dx
    for i in range(0, 2):
        for j in range(2, 7):
            u_grid[i][i + j] = 1
        for j in range(7, 12):
            u_grid[i][i + j] = -1

    for i in range(1, 999):
        for j in range(1, 999):
            with np.errstate(divide="ignore", invalid="ignore"):
                ctrldfr = (
                    u_grid[i][j + 1] - 2 * u_grid[i][j] + u_grid[i][j - 1]
                ) / Dx**2
                u_grid[i + 1][j] = (
                    Dt**2 * ctrldfr + 2 * u_grid[i][j] - u_grid[i - 1][j]
                )
    u_grid[
        u_grid == 0
    ] = np.nan  # putting nan to zero values so they don't get plotted by matplotlib
    for i in set(20 * np.arange(1, 6)):
        fig = plt.figure()
        ax = plt.axes()
        plt.title("$\dfrac{\Delta t}{\Delta x}$" + f"={fraction_constant}")
        ax.plot(u_grid[i][:], label="$Dt$" + f"={i}")
        plt.ylabel(r"$u_{p}$")
        plt.xlabel(r"$\Delta t$")
        plt.legend()
        fig.tight_layout()
        savim("images", f"{Dx}_{fraction_constant}_dt_{i}")
        plt.close()

    fig = plt.figure()
    fig.tight_layout()
    plt.ylabel(r"$u$")
    plt.xlabel(r"$\Delta t$")
    ax = plt.axes()
    # ax.xaxis.set_ticklabels(np.arange(0, 1.1, 0.1).round(1))
    ax.plot(u_grid[0, :])

    def update(i):
        fig.clear()
        plt.title(r"$\dfrac{\Delta t}{\Delta x}=$" + f"{fraction_constant}")
        plt.ylabel(r"$u$")
        plt.xlabel(r"$\Delta t$")
        p = plt.plot(u_grid[i, :], label="$Dt$" + f"={i}")
        fig.tight_layout()
        plt.draw()

    ani = animation.FuncAnimation(fig, update, frames=999)
    ani.save(f"./videos/hm_{Dx}_{fraction_constant}.mp4", dpi=1000, bitrate=-1)
    return u_grid


# Trying out two different Dx values to see whether there is a discrepancy.
calc(0.01, 0.9)
calc(0.01, 1)
calc(0.01, 1.1)
calc(10 ** (-8), 0.9)
calc(10 ** (-8), 1)
calc(10 ** (-8), 1.1)
