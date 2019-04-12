# -*- coding: utf-8 -*-

"""Console script for pipe_tools."""
import sys
import click
import numpy as np

from wall import wall_thicknesses


@click.command()
def main(args=None):

    P_d = 380e5
    h_ref = 24
    rho_sw = 1025
    rho_c = 10

    x = np.array([0, 1])
    location = np.array(["seabed", "seabed"])
    D_o = np.array([0.2731, 0.2731])
    h = np.array([200, 50])
    sigma_y = np.array([427e6, 427e6])
    t_corr = np.array([0.001, 0.001])
    f_tol = np.array([0.125, 0.125])
    E = np.array([207e9, 207e9])
    v = np.array([0.3, 0.3])
    f_0 = np.array([0.01, 0.01])

    wts = wall_thicknesses(
        P_d, h_ref, rho_c, x, location, D_o, h, sigma_y, t_corr, f_tol, E, v, f_0
    )

    from tabulate import tabulate

    headers = ["KP [m]", "Hoop [m]", "Collapse [m]", "Buckle [m]", "Required [m]"]
    print(tabulate(np.transpose(wts), headers, tablefmt="psql"))

    from plot import plot_wall_thicknesses

    plot = plot_wall_thicknesses(wts)
    plot.savefig("wall_plot.png")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
