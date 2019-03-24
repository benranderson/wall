import matplotlib.pyplot as plt

plt.style.use("seaborn-pastel")


def plot_wall_thicknesses(wts):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(wts[0], 1000 * wts[1], label="Hoop")
    ax.plot(wts[0], 1000 * wts[2], label="Collapse")
    ax.plot(wts[0], 1000 * wts[3], label="Buckle")
    ax.set_xlabel("KP [m]")
    ax.set_ylabel("Nominal Wall Thickness [mm]")
    ax.legend()
    ax.grid()
    plt.tight_layout()
    return plt
