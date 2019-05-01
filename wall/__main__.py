# -*- coding: utf-8 -*-

"""Console script for pipe_tools."""
import sys
import click
import numpy as np
import pandas as pd
from tabulate import tabulate

from wall import wall_thicknesses
from wall import plot_wall_thicknesses


@click.command()
def main(args=None):

    P_d = 380e5
    h_ref = 24
    rho_sw = 1025
    rho_c = 100

    i = pd.read_csv("InputData.csv")

    x = i["KP"].values
    location = i["Location"].values
    D_o = i["D_o"].values
    h = i["h"].values
    sigma_y = i["sigma_y"].values
    t_corr = i["t_corr"].values
    f_tol = i["f_tol"].values
    E = i["E"].values
    v = i["v"].values
    f_0 = i["f_0"].values

    wts = wall_thicknesses(
        P_d,
        h_ref,
        rho_c,
        x,
        location,
        D_o,
        h,
        sigma_y,
        t_corr,
        f_tol,
        E,
        v,
        f_0,
        rho_sw,
    )

    headers = ["KP [m]", "Hoop [m]", "Collapse [m]", "Buckle [m]", "Required [m]"]
    print(tabulate(np.transpose(wts), headers, tablefmt="psql"))

    plot = plot_wall_thicknesses(wts)
    plot.savefig("wall_plot.png")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
