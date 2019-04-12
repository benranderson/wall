import pytest
import numpy as np
import wall as w


test_data = {
    "D_o": np.array([0.1683, 0.2731]),
    "P_d": np.array([345e5, 214e5]),
    "h": np.array([95, 94]),
    "h_ref": np.array([0, 0]),
    "rho_c": np.array([750, 1050]),
    "sigma_y": np.array([508.4e6, 475e6]),
    "location": np.array(["seabed", "seabed"]),
    "t_corr": np.array([0.001, 0]),
    "f_tol": np.array([0.125, 0.125]),
    "E": np.array([207e9, 199e9]),
    "v": np.array([0.3, 0.3]),
    "f_0": np.array([0.025, 0.025]),
    "P_h": np.array([6.99e5, 9.682e5]),
    "P_i": np.array([3.5199e7, 223.682e5]),
    "hoop_min": np.array([0.007872, 0.008554]),
    "hoop_nom": np.array([0.01014, 0.009775]),
    "collapse_nom": np.array([0.00288, 0.00473]),
    "buckle_nom": np.array([0.003606, 0.006002]),
}


def test_pressure_head():
    P_h = w.pressure_head(test_data["h"], test_data["rho_c"])
    assert pytest.approx(P_h, rel=1e-3) == test_data["P_h"]


def test_internal_pressure():
    P_i = w.internal_pressure(
        test_data["P_d"], test_data["h"], test_data["rho_c"], test_data["h_ref"]
    )
    assert pytest.approx(P_i, rel=1e-3) == test_data["P_i"]


@pytest.fixture
def P_e():
    return w.pressure_head(test_data["h"], 1025)


@pytest.fixture
def delta_P(P_e):
    P_i = w.internal_pressure(
        test_data["P_d"], test_data["h"], test_data["rho_c"], test_data["h_ref"]
    )
    return abs(P_i - P_e)


def test_min_hoop_thickness(delta_P):
    t_min, _ = w.min_hoop_thickness(
        test_data["D_o"], delta_P, test_data["sigma_y"], test_data["location"]
    )
    assert pytest.approx(t_min, rel=1e-3) == test_data["hoop_min"]


def test_nom_hoop_thickness(delta_P):
    t_min, _ = w.min_hoop_thickness(
        test_data["D_o"], delta_P, test_data["sigma_y"], test_data["location"]
    )
    t_nom = w.nom_hoop_thickness(t_min, test_data["t_corr"], test_data["f_tol"])
    assert pytest.approx(t_nom, rel=1e-3) == test_data["hoop_nom"]


def test_collapse_thickness(P_e):
    t_nom = w.v_collapse_thickness(
        P_e,
        test_data["sigma_y"],
        test_data["E"],
        test_data["v"],
        test_data["D_o"],
        test_data["f_0"],
    )
    assert pytest.approx(t_nom, rel=1e-3) == test_data["collapse_nom"]


def test_buckle_thickness(P_e):
    t_nom = w.buckle_thickness(test_data["D_o"], P_e, test_data["sigma_y"])
    assert pytest.approx(t_nom, rel=1e-3) == test_data["buckle_nom"]
