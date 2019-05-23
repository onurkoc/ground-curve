from Intersection import intersection
from collections import namedtuple
from Rate_of_Flow import rate_of_flow as rof
import numpy as np


def ground_curve(gamma=24.4, H=400, nu=0.3, E=100000, D=5.5, c=625, phi=23.79,
                 f_ck=25, E_c=15000, nu_c=0.2, t_c=0.2, dis_sup=1,
                 advance_rate=5):
    """
    # --------------------------------
    # Input values for rock/soil
    # --------------------------------
    gamma        - [kN/m³] - specific weight of the rock mass
    H            - [m]     - overburden
    nu           - [-]     - Poisson's ratio of the rock
    E            - [kPa]   - Modulus of elasticity of the rock
    D            - [m]     - Diameter of the tunnel
    c            - [kPa]   - Cohesion
    phi          - [deg]   - Friction angle
    # --------------------------------
    # Input values for support members
    # --------------------------------
    f_ck         - [MPa]   - Uniaxial compressive strength of the
                             sprayed concrete
    E_c          - [MPa]   - Young's modulus of the sprayed concrete
    nu_c         - [-]     - Poisson's ratio of the sprayed concrete
    t_c          - [m]     - Thickness of the sprayed concrete
    dis_sup      - [m]     - Distance of the support member to the face
    advance_rate - [m/day] - Rate of advance
    """
    p_o = gamma * H  # [kPa]   - in situ stress
    Phi = np.deg2rad(phi)  # [rad] - conversion from degrees to radians
    p_i = np.linspace(0, p_o, 1000)
    # [kPa] - Support pressure (an array from zero to insitu stress)
    sigma_cm = 2 * c * np.cos(Phi) / (1 - np.sin(
        Phi))  # [kPa] - the uniaxial strength of the rock mass
    k = (1 + np.sin(Phi)) / (1 - np.sin(
        Phi))  # [-] - slope defined by the Mohr-Coulomb criterion

    # Analysis of tunnel behaviour:

    #############################
    # a. Tunnel wall displacement
    #############################

    p_cr = (2 * p_o - sigma_cm) / (1 + k)
    # [kPa] - critical support pressure
    # if the critical support pressure is smaller than the internal
    # support pressure then failure does not occur

    r_o = D / 2
    # [m] - radius of the tunnel

    u_ie = r_o * (1 + nu) / E * (p_o - p_i)
    # [m] - inward radial elastic displacement (Pi is a variable)

    r_p = r_o * (2 * (p_o * (k - 1) + sigma_cm) / (1 + k) / (
                (k - 1) * p_i + sigma_cm)) ** (1 / (k - 1))

    r_p = np.where(p_i < p_cr, r_p, r_o)
    # [m] - radius of the plastic zone
    # if the support pressure is higher than critical pressure then the
    # plastic radius is equal to tunnel radius

    u_ip = r_o * (1 + nu) / E * (
        2 * (1 - nu) * (p_o - p_cr) * (r_p / r_o) ** 2 - (
            1 - 2 * nu) * (p_o - p_i))
    # [m] - inward radial plastic displacement (Pi is a variable)

    x = np.where(p_i > p_cr, u_ie, u_ip)

    #####################################
    # b. Longitudinal displacement profile
    #####################################

    r_pm = r_o * ((2 * (p_o * (k - 1) + sigma_cm)) / ((1 + k) * sigma_cm)) ** (
        1 / (k - 1))
    # Maximum plastic zone radius [m]

    u_im = r_o * (1 + nu) / E * (
        2 * (1 - nu) * (p_o - p_cr) * (r_pm / r_o) ** 2 - (
            1 - 2 * nu) * (p_o))
    # Maximum displacement [m] - r_p = r_pm; p_i = 0

    u_if = (u_im / 3) * np.exp(-0.15 * (r_pm / r_o))
    # Displacement at the tunnel face (by Vlachopoulus and Diederichs) [m]

    # Displacement ahead of the face

    x_ = np.arange(-25, 80, 0.1)
    # Distance from tunnel face (an array from -25m ahead and 80m behind the
    # face) [m]

    u_ix_a = (u_if) * np.exp(x_ / r_o)
    # Tunnel wall displacement ahead of the face (x < 0) [m]

    # Displacement behind the face

    u_ix_b = u_im * (1 - (1 - u_if / u_im) * np.exp(
        (-3 * x_ / r_o) / (2 * r_pm / r_o)))
    # Tunnel wall displacement behind the face (x > 0) [m]

    x_disp = np.where(x_ < 0, u_ix_a, u_ix_b)
    # x values for displacement

    ################################################
    # c. Calculate the actual/target strength of SCL
    ################################################

    x_sup = np.arange(dis_sup, 80, 1)
    # Distance from installation of SCL

    u_io = u_im * (1 - (1 - u_if / u_im) * np.exp(
        (-3 * dis_sup / r_o) / (2 * r_pm / r_o)))
    # Tunnel wall displacement behind SCL x > distance support [m]

    time_672hours = np.arange(0, 28 * 24, 1)  # [hours]
    time_28days = time_672hours / 24  # [days]

    # Strength evolution of SCL acc. Aldrian
    sigma = np.array([f_ck * 0.03 * time if time < 8 else f_ck * np.sqrt(
        (time - 5) / (45 + 0.925 * time))
        for time in time_672hours])

    # change of elasticity in time
    E_28 = E_c  # [MPa]
    P_Ar1 = 1
    P_Ar2 = 0.3
    P_Ar3 = 0.2
    E_t = E_28 * (time_28days / (P_Ar1 + P_Ar2 * time_28days)) ** P_Ar3

    p_scmax = sigma / 2 * (1 - ((D / 2 - t_c) ** 2 / (D / 2) ** 2))
    # maximum support pressure

    k_sc = E_t * ((D / 2) ** 2 - (D / 2 - t_c) ** 2) / (
        2 * (1 - nu_c ** 2) * (D / 2 - t_c) * (D / 2) ** 2)
    # stiffness of the support

    p_scmax_el = f_ck / 2 * (1 - ((D / 2 - t_c) ** 2 / (D / 2) ** 2))
    k_sc_el = E_c * ((D / 2) ** 2 - (D / 2 - t_c) ** 2) / (
        2 * (1 - nu_c ** 2) * (D / 2 - t_c) * (D / 2) ** 2)
    # elastic design

    x_support = u_io + p_scmax[1:] / k_sc[1:]
    y_support = p_scmax[1:]

    # find the intersection of support & ground curves
    x_int, y_int = intersection(x_support, y_support, x, p_i / 1000)

    ratio_sc = p_scmax_el / k_sc_el
    u_iy = u_io + ratio_sc
    # displacement at the yield surface of support
    x_support_el = [u_io, u_iy, u_iy * 1.002]
    y_support_el = [0, p_scmax_el, p_scmax_el]

    x_sup_intersect = np.linspace(u_io, u_iy, len(x))
    y_sup_intersect = np.linspace(0, p_scmax_el, len(x))

    # find the intersection of support & ground curves
    x_int_el, y_int_el = intersection(x_sup_intersect, y_sup_intersect, x,
                                      p_i / 1000)

    # define for convenience named tuples
    Plot = namedtuple('Plot', 'x y')
    Var = namedtuple('Variable', 'name val')
    # assign defined named tuples to variables
    # plot variables
    p1 = Plot(x=x, y=p_i/1000)
    p2 = Plot(x=x_support, y=y_support)
    p2_el = Plot(x=x_support_el, y=y_support_el)
    p3 = Plot(x=x_int, y=y_int)
    p3_el = Plot(x=x_int_el, y=y_int_el)
    p4 = Plot(x=x_disp, y=x_)
    p5 = Plot(x=time_28days[1:], y=y_support)
    p6 = Plot(x=x, y=r_p)

    # needed variables
    v1 = Var(name='P_sc_max', val=p_scmax)
    v1_el = Var(name='P_sc_max_el', val=p_scmax_el)
    if len(y_int != 0):
        v2 = Var(name='y_int', val=y_int[0])
    else:
        v2 = Var(name='y_int', val=None)
    if len(y_int_el != 0):
        v2_el = Var(name='y_int_el', val=y_int_el[0])
    else:
        v2_el = Var(name='y_int_el', val=None)
    v3 = Var(name='dis_sup', val=dis_sup)

    if len(p3.x) != 0:
        # find the radius of plastic zone at the equilibrium point
        r_pl_sup = r_o * (2 * (p_o * (k - 1) + sigma_cm) / (1 + k) / (
            (k - 1) * y_int[0] * 1000 + sigma_cm)) ** (1 / (k - 1))

        p_point = p_i[np.where(x >= x_int[0])]
        x_updated = np.linspace(0, 80, len(p_point))
        p_scl = np.linspace(x_support[0], x_int[0], len(p_point))
        p_point_x = []
        r_pl_inc = []
        p_x_l = []
        p_y_l = []

        for p_scl_inc, p_inc in zip(p_scl, p_point):
            r_pl_sup_inc = r_o * (2 * (p_o * (k - 1) + sigma_cm) / (1 + k) / (
                (k - 1) * p_inc + sigma_cm)) ** (1 / (k - 1))
            r_pl_inc.append(r_pl_sup_inc)
            u_im_inc = r_o * (1 + nu) / E * (
                2 * (1 - nu) * (p_o - p_cr) * (r_pl_sup_inc / r_o) ** 2 - (
                    1 - 2 * nu) * (p_o))
            u_if_inc = (u_im_inc / 3) * np.exp(-0.15 * (r_pl_sup_inc / r_o))
            u_ix_b_inc = u_im_inc * (1 - (1 - u_if_inc / u_im_inc) * np.exp(
                (-3 * x_updated / r_o) / (2 * r_pl_sup_inc / r_o)))
            p_point_x.append(u_ix_b_inc)
            # intersection points with vertical lines
            p_ver_x = np.array([p_scl_inc, p_scl_inc])
            p_ver_y = np.array([0, 50])
            x1, y1 = intersection(p_ver_x, p_ver_y, u_ix_b_inc, x_updated)
            if len(x1) != 0 or len(y1) != 0:
                p_x_l.append(x1)
                p_y_l.append(y1)
        p_point_x = np.array(p_point_x)
        p_x_l = np.array(p_x_l)
        p_y_l = np.array(p_y_l)

        # update the longitudinal displacement behind the face
        u_im_updated = r_o * (1 + nu) / E * (
            2 * (1 - nu) * (p_o - p_cr) * (r_pl_sup / r_o) ** 2 - (
                1 - 2 * nu) * (p_o))
        # Maximum displacement [m] - r_p = r_pm; p_i = 0
        u_if_updated = (u_im_updated / 3) * np.exp(-0.15 * (r_pl_sup / r_o))
        # Displacement at the tunnel face (by Vlachopoulus and Diederichs) [m]
        u_ix_b_updated = u_im_updated * (
            1 - (1 - u_if_updated / u_im_updated) * np.exp(
                (-3 * x_updated / r_o) / (2 * r_pl_sup / r_o)))
        # Tunnel wall displacement behind the face (x > 0) [m]
        p7 = Plot(x=u_ix_b_updated, y=x_updated)
        p8 = Plot(x=p_point_x, y=x_updated)
        p9 = Plot(x=p_x_l, y=p_y_l)  # points of the intersection of the curves
        sigma_actual, arr_hours = rof(disp_array_2d=p9, rate=advance_rate)
        p10 = Plot(x=arr_hours/24, y=sigma_actual)
        p11 = Plot(x=time_672hours/24, y=sigma)
        return p1, p2, p2_el, p3, p3_el, p4, p5, p6, p7, p8, p9, p10, p11, \
            v1, v1_el, v2, v2_el, v3

    return p1, p2, p2_el, p3, p3_el, p4, p5, p6, v1, v1_el, v2, v2_el, v3


if __name__ == '__main__':
    values = ground_curve()
    if len(values) == 9:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, v1, v1_el, v2, v2_el, v3 = values
    else:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, p7, p8, p9, p10, p11, v1, \
            v1_el, v2, v2_el, v3 = values
    print(p1)
