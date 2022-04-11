import sympy as sp
import matplotlib.pyplot as plt  # needed for graphs
import pathlib  # needed to create folder
import numpy as np
from tqdm import tqdm


Dt, Dx, l, c, y = sp.symbols("Dt Dx l c y")


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
w = 2 * sp.pi * c * Dx
wrpl = 2 * sp.pi * c / l
ktilde = sp.acos((Dx / (c * Dt)) ** 2 * (sp.cos(wrpl * Dt) - 1) + 1) * l
u_p = w / ktilde


def subs_coeff_eval(a: int) -> sp.core.mul.Mul:
    """subs_coeff_eval Substitutes a constant based on the time-step

    Args:
        a (int): Ranging from 0 to 1 (0,1)

    Returns:
        sp.core.mul.Mul: Final equation ready to get lambdified
    """
    u_p_temp = u_p.subs(Dt, Dx / (c * a))
    u_p_final = u_p_temp.subs([(Dx / l, y), (c, 3 * 10**8)])
    return u_p_final


# (a) = / 2c
u_p_a1 = subs_coeff_eval(2)
# (b) = / 4c
u_p_b1 = subs_coeff_eval(4)
# (c) = / 8c
u_p_c1 = subs_coeff_eval(8)
x = np.linspace(0, 0.4, 10000)
with np.errstate(divide="ignore", invalid="ignore"):  # RuntimeWarning: divide by zero
    f_a = sp.lambdify(y, u_p_a1)(x)
    f_b = sp.lambdify(y, u_p_b1)(x)
    f_c = sp.lambdify(y, u_p_c1)(x)
# Time to plot our graphs
fig = plt.figure()
ax = plt.axes()
plt.ylabel(r"$u_{p}$")
plt.xlabel(r"$\dfrac{\Delta x}{\lambda}$")
plt.title(r"Numerical phase velocity versus $\frac{\Delta x}{\lambda}$")
ax.set
ax.set_xscale("log")
plt.plot(
    x,
    f_a,
    alpha=0.5,
    label=r"$\Delta t = \dfrac{\Delta x}{2}$",
    color="#35063e",
    zorder=2,
)
plt.plot(
    x,
    f_b,
    alpha=1,
    label=r"$\Delta t = \dfrac{\Delta x}{4}$",
    color="#dbb40c",
)
plt.plot(
    x,
    f_c,
    alpha=0.5,
    label=r"$\Delta t = \dfrac{\Delta x}{8}$",
    color="#0165fc",
    zorder=2,
)
fig.tight_layout()
ax_new = fig.add_axes([0.5, 0.4, 0.3, 0.3])
ax_new.set_xscale("log")
plt.plot(x, f_a, alpha=0.7, label=r"$\Delta t = \dfrac{\Delta x}{2}$", color="#35063e")
plt.plot(
    x,
    f_b,
    alpha=1,
    label=r"$\Delta t = \dfrac{\Delta x}{4}$",
    color="#dbb40c",
)
plt.plot(
    x,
    f_c,
    alpha=0.7,
    label=r"$\Delta t = \dfrac{\Delta x}{8}$",
    color="#0165fc",
    zorder=2,
)
plt.xlim(0.2, 0.35)
ax_new.tick_params(axis="x", which="major", labelsize=10)
ax_new.tick_params(axis="x", which="minor", labelsize=10)
ax.legend()
savim("images", "prob1_task1")
print(
    "Numerical phase velocity equals to:\n"
    + f"(a) {u_p_a1.subs(y,0.1).evalf():.6e}\n"
    + f"(b) {u_p_b1.subs(y,0.1).evalf():.6e}\n"
    + f"(c) {u_p_c1.subs(y,0.1).evalf():.6e}"
)
