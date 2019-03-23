import matplotlib.pyplot as plt

plt.style.use("seaborn-pastel")


def plot_wall_thicknesses(x, hoop, collapse, buckle):
    fig, ax1 = plt.subplots(figsize=(8, 4))
    # ax2 = ax1.twinx()
    ax1.plot(x, 1000 * hoop, label="Hoop")
    ax1.plot(x, 1000 * collapse, label="Collapse")
    ax1.plot(x, 1000 * buckle, label="Buckle")
    ax1.set_xlabel("KP [m]")
    ax1.set_ylabel("Nominal Wall Thickness [mm]")
    ax1.legend()
    ax1.grid()
    plt.tight_layout()
    return plt
