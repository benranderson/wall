import pytest
import numpy as np
import wall as w


test_data = {
    "D_o": np.array([0.2731, 0.2731]),
    "P_d": np.array([380e5, 380e5]),
    "h": np.array([96.8, 87]),
    "h_ref": 24,
    "rho_c": np.array([982.7, 982.7]),
    "sigma_y": np.array([427e6, 427e6]),
    "location": np.array(["seabed", "seabed"]),
    "P_i": np.array([391.645e5, 390.701e5]),
    "hoop_min": np.array([0.016029, 0.016031]),
}


def test_internal_pressure():
    P_i = w.internal_pressure(
        test_data["P_d"], test_data["h"], test_data["rho_c"], test_data["h_ref"]
    )
    assert pytest.approx(P_i, abs=100) == test_data["P_i"]


@pytest.fixture
def delta_P():
    P_i = w.internal_pressure(
        test_data["P_d"], test_data["h"], test_data["rho_c"], test_data["h_ref"]
    )
    P_e = w.pressure_head(test_data["h"], 1025)
    return abs(P_i - P_e)


def test_min_hoop_thickness(delta_P):
    hoop_min, ratio = w.min_hoop_thickness(
        test_data["D_o"], delta_P, test_data["sigma_y"], test_data["location"]
    )
    assert pytest.approx(hoop_min, abs=1e-6) == test_data["hoop_min"]

