import numpy as np
import typing


def rate_of_flow(disp_array_2d: typing.NamedTuple, rate: float):
    """calculate the actual displacement of the scl using the data
    calculated by the ground curve"""

    wall_disp, dist_to_face = disp_array_2d
    arr_disp = wall_disp - wall_disp[0]
    arr_dist_to_scl = dist_to_face - dist_to_face[0]
    # subtract the initial displacement of the wall and the initial
    # displacement of the scl to set it zero

    # Calculate the time from advance rate
    arr_days = arr_dist_to_scl / rate
    arr_hours = arr_days * 24

    del_eps = arr_disp[1:] - arr_disp[:-1]

    # Constants for rate of flow calculation
    E_28 = 15000  # [MPa]
    A = 0.0001  # [1/MPa*d^(1/3)]
    B = 600  # [d]
    eps_sh_inf = 0.00125
    C_d_inf = 0.00009  # [1/MPa]
    Q = 0.0001  # [1/MPa]

    # delta C_t
    C_t = A * arr_days ** (1 / 3)

    # strains due to temperature
    eps_t = (-1 * np.cos(
        np.deg2rad(arr_days ** 0.25 * 250)) + 1) * 30 / 1000000

    # change of elasticity in time
    P_Ar1 = 1
    P_Ar2 = 0.3
    P_Ar3 = 0.2
    E_t = E_28 * (arr_days / (P_Ar1 + P_Ar2 * arr_days)) ** P_Ar3

    # strains due to shrinkage
    eps_sh = eps_sh_inf * arr_days / (arr_days + B)

    sigma_2 = [0]
    eps_d = [0]
    for i, _ in enumerate(arr_days):
        try:
            if i == 0:
                value_eps_d = 0
                eps_d.append(value_eps_d)
                value_sigma_2 = 0
                sigma_2.append(value_sigma_2)
            else:
                del_eps_sh = eps_sh[i] - eps_sh[i-1]
                del_eps_t = eps_t[i] - eps_t[i-1]
                del_C_t = C_t[i] - C_t[i-1]
                value_eps_d = (sigma_2[i - 1] * C_d_inf - eps_d[i - 1]) * (
                            1 - np.exp(-del_C_t / Q))
                eps_d.append(value_eps_d)
                value_sigma_2 = ((del_eps[i] - del_eps_sh - del_eps_t
                                  + eps_d[i - 1] * (1 - np.exp(-del_C_t /
                                                               Q)) +
                                  sigma_2[i - 1] / E_t[i]) / (C_d_inf * (
                        1 - np.exp(-del_C_t / Q)) + del_C_t + (1 /E_t[i])
                                                              )
                                 )
                sigma_2.append(value_sigma_2)
        except IndexError:
            pass

    sigma_actual = np.array(sigma_2)

    return sigma_actual, arr_hours