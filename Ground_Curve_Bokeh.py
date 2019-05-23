# -*- coding: utf-8 -*-
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Slider
import numpy as np

from Ground_Curve import ground_curve as gc

values = gc()
if len(values) == 13:
    p1, p2, p2_el, p3, p3_el, p4, p5, p6, v1, v1_el, v2, v2_el, v3 = values
else:
    p1, p2, p2_el, p3, p3_el, p4, p5, p6, p7, p8, p9, p10, p11, v1, \
        v1_el, v2, v2_el, v3 = values

source1 = ColumnDataSource(data=dict(
    x=p1.x,
    y=p1.y
))

source2 = ColumnDataSource(data=dict(
    x=p2_el.x,
    y=p2_el.y
))

if p3_el.y is not None:
    safety = [
        f'F.S. = {np.round([max(p2_el.y) / p3_el.y], 2).flatten()[0]}']
else:
    safety = []

source3 = ColumnDataSource(data=dict(
    x=p3_el.x,
    y=p3_el.y,
    safety=safety
))

gamma_slider = Slider(title="Gamma [kN/m³]",
                      value=24.4, start=15, end=30, step=0.1)
overburden_slider = Slider(title="Overburden [m]",
                           value=400, start=10, end=1000, step=10)
e_module_slider = Slider(title="E Module [kPa]",
                         value=100000, start=10000, end=3000000, step=10000)
nu_slider = Slider(title="Nu [-]",
                   value=0.3, start=0.1, end=0.49, step=0.01)
diameter_slider = Slider(title="Diameter [m]",
                         value=5.5, start=3, end=20, step=0.1)
cohesion_slider = Slider(title="Cohesion [kPa]",
                         value=625, start=1, end=2000, step=10)
phi_slider = Slider(title="Phi [°]",
                    value=23.79, start=15, end=40, step=0.1)

f_ck_slider = Slider(title="Concrete Strength [MPa]",
                     value=25, start=15, end=30, step=1)
e_conc_slider = Slider(title="Concrete Elasticity [MPa]",
                       value=15000, start=5000, end=30000, step=1000)
thickness_slider = Slider(title="Concrete Thickness [m]",
                          value=0.2, start=0, end=0.5, step=0.05)
dist_sup_slider = Slider(title="Support-Face Distance [m]",
                         value=1, start=0, end=5, step=0.1)
advance_rate_slider = Slider(title="Advance Rate [m/day]",
                             value=5, start=0.5, end=10, step=0.5)

def update_input(attr, old, new):
    # Get the current slider values
    gamma = float(gamma_slider.value)
    overburden = float(overburden_slider.value)
    nu = float(nu_slider.value)
    e_module = float(e_module_slider.value)
    cohesion = float(cohesion_slider.value)
    diameter = float(diameter_slider.value)
    phi = float(phi_slider.value)
    f_ck = float(f_ck_slider.value)
    e_conc = float(e_conc_slider.value)
    thickness = float(thickness_slider.value)
    dist_sup = float(dist_sup_slider.value)
    advance_rate = float(advance_rate_slider.value)
    values = gc(gamma=gamma, H=overburden, nu=nu, E=e_module, D=diameter,
                c=cohesion, phi=phi,
                f_ck=f_ck, E_c=e_conc, nu_c=0.2, t_c=thickness,
                dis_sup=dist_sup,
                advance_rate=advance_rate)
    if len(values) == 13:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, v1, v1_el, v2, v2_el, v3 = values
    else:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, p7, p8, p9, p10, p11, v1, \
            v1_el, v2, v2_el, v3 = values
    source1.data = dict(x=p1.x, y=p1.y)
    source2.data = dict(x=p2_el.x, y=p2_el.y)
    if v2_el.val is not None:
        safety = [
            f'F.S. = {np.round([max(p2_el.y) / p3_el.y], 2).flatten()[0]}'
        ]
    else:
        safety = []
    source3.data = dict(x=p3_el.x, y=p3_el.y, safety=safety)


for widget in [gamma_slider, overburden_slider, overburden_slider, nu_slider,
               e_module_slider, cohesion_slider, phi_slider, diameter_slider,
               f_ck_slider, e_conc_slider, thickness_slider, dist_sup_slider]:
    widget.on_change('value', update_input)

inputs = widgetbox(gamma_slider,
                   overburden_slider,
                   nu_slider,
                   e_module_slider,
                   cohesion_slider,
                   phi_slider,
                   diameter_slider,
                   f_ck_slider,
                   e_conc_slider,
                   thickness_slider,
                   dist_sup_slider,
                   advance_rate_slider)

p1 = figure(plot_width=600, plot_height=400)

p1.title.text = 'Ground Reaction Curve'
p1.xaxis.axis_label = 'Tunnel Wall Displacement [m]'
p1.yaxis.axis_label = 'Support Pressure [MPa]'
p1.y_range.start = 0
p1.x_range.start = 0
p1.background_fill_color = "lightgray"
p1.background_fill_alpha = 0.05
p1.xgrid.grid_line_alpha = 0.7
p1.xgrid.grid_line_dash = [6, 4]
p1.ygrid.grid_line_alpha = 0.7
p1.ygrid.grid_line_dash = [6, 4]

line1 = p1.line('x', 'y', line_width=2,
                line_color='blue', source=source1, legend='Ground Curve')
line2 = p1.line('x', 'y', line_width=2,
                line_color='red', source=source2, legend='Support Curve')

circle = p1.circle(
    'x', 'y', fill_color="white", size=5,
    legend='safety', source=source3
)

curdoc().add_root(row(inputs, p1))
curdoc().title = "Ground Reaction Curve"
