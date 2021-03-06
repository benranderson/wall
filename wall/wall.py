import numpy as np
from scipy.optimize import newton

DESIGN_FACTORS = {"riser": 0.6, "seabed": 0.72}


def pressure_head(h, rho, g=9.81):
    """Calculate the fluid pressure head.

    Parameters
    ----------
    h : array : Water depth [m]
    rho : array : Fluid density [kg/m^3]
    g : float : Acceleration of gravitiy [m/s/s]

    Returns
    -------
    P_h : array : Pressure head [Pa]
    """
    return rho * g * h


def internal_pressure(P_d, h, rho_c, h_ref=0):
    """Calculate the internal pressure of the pipeline at the seabed.

    Parameters
    ----------
    P_d : array : Design pressure [Pa]
    h : array : Water depth [m]
    rho_c : array : Contents density [kg/m^3]
    h_ref : array : Reference height [m]

    Returns
    -------
    P_i : array : Internal pressure [Pa]
    """
    P_h = pressure_head(h + h_ref, rho_c)
    return P_d + P_h


def min_hoop_thickness(D_o, delta_P, sigma_y, location):
    """Calculate the minimum wall thickness for hoop stress considering
    thin wall and thick wall equations (PD 8010-2 Section 6.4.2).    
    
    Parameters
    ----------
    D_o : array : Outside diameter [m]
    delta_P : array : Pressure difference [Pa]
    sigma_y : array : Derated yield strength [Pa]
    location : array : Pipeline location (seabed or riser)

    Returns
    -------
    t_min : array : Minimum wall thickness [m]
    ratio : array : D_o / t_min ratio [-]
    """

    # hoop stress design factor
    f_d = np.vectorize(DESIGN_FACTORS.get)(location)

    # allowable stress (PD 8010-2 equation 2)
    sigma_a = f_d * sigma_y

    # thin wall equation (PD 8010-2 equation 3)
    thin = delta_P * D_o / (2 * sigma_a)

    def thick():
        # thick wall equation (PD 8010-2 equation 5)
        return 0.5 * (
            D_o
            - np.sqrt(((sigma_a - abs(delta_P)) * D_o ** 2) / (sigma_a + abs(delta_P)))
        )

    ratio = D_o / thin
    t_min = np.where(ratio > 20, thin, thick())

    return t_min, ratio


def nom_hoop_thickness(t_min, t_corr, f_tol):
    """Calculate the nominal wall thickness considering mechanical allowances
    (PD 8010-2 equation 4).
    
    Parameters
    ----------
    t_min : array : Minimum wall thickness [m]
    t_corr : array : Corrosion allowance [m]
    f_tol : array : Fabrication tolerance [-]

    Returns
    -------
    t_nom : array : Nominal wall thickness [m]
    """

    # return zero if denominator is zero (i.e. 100% f_tol)
    return np.where(1 - f_tol, (t_min + t_corr) / (1 - f_tol), 0)


def collapse_thickness(P_e, sigma_y, E, v, D_o, f_0, f_s=2):
    """Calculate the nominal wall thickness for local buckling due to external
    pressure (PD8010-2 Clause G.1.2).

    Parameters
    ----------
    P_e : array : External pressure [Pa]
    sigma_y : array : Pipe yield strength [Pa]
    E : array : Young's modulus [Pa]
    v : array : Poisson's ratio [-]
    D_o : array : Outside diameter [m]
    f_0 : array : Pipeline ovality [-]  
    float f_s: Factor of safety [-]

    Returns
    -------
    t_nom : array : Nominal wall thickness [m] 
    """

    # characteristic external pressure
    P_char = f_s * P_e

    def P_cr(t):
        """Calculate the critical pressure for an elastic critical tube
        (PD8010-2 Equation G.2).
        """
        return 2 * E / (1 - v * v) * (t / D_o) ** 3

    def P_y(t):
        """Calculate the yield pressure (PD8010-2 Equation G.3).
        """
        return 2 * sigma_y * (t / D_o)

    def char_resist(t):
        """Calculate the characteristic resistance for external pressure
        (PD8010-2 Equation G.1).       
        """
        term_1 = (P_char / P_cr(t)) - 1
        term_2 = (P_char / P_y(t)) ** 2 - 1
        return term_1 * term_2 - (P_char / P_y(t)) * f_0 * (D_o / t)

    return newton(char_resist, 1e-3)


v_collapse_thickness = np.vectorize(collapse_thickness)


def buckle_thickness(D_o, P_p, sigma_y):
    """Calculate the nominal buckle thickness based on the propagation pressure
    (PD8010-2 Equation G.21).

    Parameters
    ----------
    D_o : array Outside Diameter [m]
    P_p : array Propagation pressure [Pa]
    sigma_y : array Yield strength [Pa]

    Returns
    -------
    t_nom : array Nominal wall thickness [m] 
    """
    return D_o * (P_p / (10.7 * sigma_y)) ** (4 / 9)


def wall_thicknesses(
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
    rho_sw=1025,
):
    """Calculate nominal wall thicknesses in accordance with PD 8010-2.
    """

    P_i = internal_pressure(P_d, h, rho_c, h_ref)
    P_e = pressure_head(h, rho_sw)
    delta_P = abs(P_i - P_e)
    hoop_min, _ = min_hoop_thickness(D_o, delta_P, sigma_y, location)
    hoop_nom = nom_hoop_thickness(hoop_min, t_corr, f_tol)
    collapse_nom = v_collapse_thickness(P_e, sigma_y, E, v, D_o, f_0)
    buckle_nom = buckle_thickness(D_o, P_e, sigma_y)
    required = np.maximum.reduce([hoop_nom, collapse_nom, buckle_nom])

    return np.array([x, hoop_nom, collapse_nom, buckle_nom, required])


if __name__ == "__main__":  # pragma: no cover
    wts = wall_thicknesses(
        P_d=100e5,
        h_ref=0,
        rho_c=900,
        x=1,
        location="seabed",
        D_o=0.1,
        h=100,
        sigma_y=450e6,
        t_corr=0,
        f_tol=0.125,
        E=207e9,
        v=0.3,
        f_0=0.025,
        rho_sw=1025,
    )
    print(wts)
