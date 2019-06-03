import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from Ground_Curve import ground_curve as gc
from Draw_graph_copy import draw
from textwrap import dedent


app = dash.Dash(__name__)

app.title = 'Ground Reaction Curve'

server = app.server


def header(title):
    return html.Div(
        style={'borderBottom': 'thin lightgrey solid', 'marginRight': 20,
               'marginLeft': 10},
        children=[html.Div(title, style={'fontSize': 25,
                                         'font-family': 'Arial'})]
    )


def row(children=None, **kwargs):
    return html.Div(
        children,
        className="row",
        **kwargs
    )


def column(children=None, width=1, **kwargs):
    number_mapping = {
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
        7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven',
        12: 'twelve'
    }
    return html.Section(
        children,
        className="{} columns".format(number_mapping[width]),
        **kwargs
    )


def named_slider(my_id, **kwargs):
    return html.Div(
        style={'margin': '10px 0px'},
        children=[
            dcc.Slider(id=my_id, **kwargs)
        ]
    )


def named_input(my_id, **kwargs):
    return html.Div(
        style={'font-family': 'Arial'},
        children=[
            dcc.Input(id=my_id, **kwargs)
        ]
    )


app.layout = html.Div([
    html.Div([
        header('Ground Reaction Curve'),
        row([
            column(width=2,
                   style={'width': '10%',
                          'display': 'inline-block',
                          'marginBottom': 0,
                          'marginTop': 40,
                          'marginLeft': 10,
                          'marginRight': 0,
                          'padding': 0,
                          'vertical-align': 'top'
                          },
                   children=[
                        html.Div([
                            html.Div('Ground Properties:', style={
                                'borderBottom': 'thin lightgrey solid',
                                'font-family': 'Arial', 'fontSize': 18
                            }),
                            html.Div(id='gamma-value-container',
                                     style={'margin': '10px 0px',
                                            'marginTop': 20}),
                            named_slider(
                                my_id='gamma_value',
                                value=20,
                                min=15,
                                max=30,
                                step=0.1
                            ),
                            html.Div(id='overburden-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='overburden_value',
                                value=200,
                                min=10,
                                max=1000,
                                step=10
                            ),
                            html.Div(id='e-module-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='e_module',
                                value=1050000,
                                min=10000,
                                max=1000000,
                                step=10000
                            ),
                            html.Div(id='nu-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='nu_value',
                                value=0.30,
                                min=0.05,
                                max=0.49,
                                step=0.01
                            ),
                            html.Div(id='cohesion-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='cohesion_value',
                                value=1000,
                                min=0,
                                max=2000,
                                step=10
                            ),
                            html.Div(id='phi-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='phi_value',
                                value=28,
                                min=15,
                                max=40,
                                step=0.1
                            ),
                            html.Div('Other Properties:', style={
                                'borderBottom': 'thin lightgrey solid',
                                'font-family': 'Arial', 'fontSize': 18
                            }),
                            html.Div(id='diameter-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='diameter_value',
                                value=5,
                                min=3,
                                max=20,
                                step=0.1
                            ),
                            html.Div(id='f_ck-value-container',
                                     style={'margin': '10px 0px',
                                            'marginTop': 20}),
                            named_slider(
                                my_id='f_ck_value',
                                value=20,
                                min=10,
                                max=40,
                                step=1
                            ),
                            html.Div(id='E_c-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='e_c_value',
                                value=5000,
                                min=5000,
                                max=35000,
                                step=1000
                            ),
                            html.Div(id='t_c-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='t_c_value',
                                value=0.2,
                                min=0,
                                max=1,
                                step=0.05
                            ),
                            html.Div(id='dis_sup-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='dis_sup_value',
                                value=2,
                                min=0,
                                max=5,
                                step=0.1
                            ),
                            html.Div(id='advance-rate-value-container',
                                     style={'margin': '10px 0px'}),
                            named_slider(
                                my_id='advance_rate_value',
                                value=5,
                                min=1,
                                max=10,
                                step=0.1
                            )
                        ])
                   ]),
            column(width=6,
                   style={'width': '50%',
                          'display': 'inline-block',
                          'marginBottom': 0,
                          'marginTop': 0,
                          'marginLeft': 0,
                          'marginRight': 0,
                          'padding': 0},
                   children=[
                       row([
                            html.Div(id='plotly-figure'),
                            row(id='Source Code',
                                style={'width': '15%',
                                       'borderTop': 'thin lightgrey solid',
                                       'marginRight': 20,
                                       'marginLeft': 10,
                                       'marginTop': 20,
                                       'fontSize': 16,
                                       'font-family': 'Arial'
                                       },
                                children=[
                                    dcc.Markdown(dedent(
                                    '''
                                    [Source Code](
                                    https://github.com/onurkoc/ground-curve)
                                    '''))]
                    )
                       ])
                   ])
        ])
    ])
])


@app.callback(
    Output('gamma-value-container', 'children'),
    [Input('gamma_value', 'value')]
)
def update_output(slider_value):
    return f'γ: {slider_value:0.1f} [kN/m³]'


@app.callback(
    Output('overburden-value-container', 'children'),
    [Input('overburden_value', 'value')]
)
def update_output(slider_value):
    return f'Overburden: {slider_value:d} [m]'


@app.callback(
    Output('e-module-container', 'children'),
    [Input('e_module', 'value')]
)
def update_output(slider_value):
    return f'E-Module: {slider_value:,} [kPa]'


@app.callback(
    Output('nu-value-container', 'children'),
    [Input('nu_value', 'value')]
)
def update_output(slider_value):
    return f'ν: {slider_value:0.2f} [-]'


@app.callback(
    Output('diameter-value-container', 'children'),
    [Input('diameter_value', 'value')]
)
def update_output(slider_value):
    return f'Tunnel Diameter: {slider_value:0.2f} [m]'


@app.callback(
    Output('cohesion-value-container', 'children'),
    [Input('cohesion_value', 'value')]
)
def update_output(slider_value):
    return f'Cohesion: {slider_value:,} [kPa]'


@app.callback(
    Output('phi-value-container', 'children'),
    [Input('phi_value', 'value')]
)
def update_output(slider_value):
    return f'φ: {slider_value:0.1f} [°]'


@app.callback(
    Output('f_ck-value-container', 'children'),
    [Input('f_ck_value', 'value')]
)
def update_output(slider_value):
    return f'SpC Strength: {slider_value:d} [MPa]'


@app.callback(
    Output('E_c-value-container', 'children'),
    [Input('e_c_value', 'value')]
)
def update_output(slider_value):
    return f'SpC Elasticity: {slider_value:,} [MPa]'


@app.callback(
    Output('t_c-value-container', 'children'),
    [Input('t_c_value', 'value')]
)
def update_output(slider_value):
    return f'SpC Thickness: {slider_value:0.2f} [m]'


@app.callback(
    Output('dis_sup-value-container', 'children'),
    [Input('dis_sup_value', 'value')]
)
def update_output(slider_value):
    return f'SpC-Face Distance: {slider_value:0.1f} [m]'


@app.callback(
    Output('advance-rate-value-container', 'children'),
    [Input('advance_rate_value', 'value')]
)
def update_output(slider_value):
    return f'Advance Rate: {slider_value:0.1f} [m/day]'


@app.callback(
    Output('plotly-figure', 'children'),
    [Input('gamma_value', 'value'),
     Input('overburden_value', 'value'),
     Input('e_module', 'value'),
     Input('nu_value', 'value'),
     Input('diameter_value', 'value'),
     Input('cohesion_value', 'value'),
     Input('phi_value', 'value'),
     Input('f_ck_value', 'value'),
     Input('e_c_value', 'value'),
     Input('t_c_value', 'value'),
     Input('dis_sup_value', 'value'),
     Input('advance_rate_value', 'value')]
)
def update_output(gamma_value, overburden_value, e_module, nu_value,
                  diameter_value, cohesion_value, phi_value, f_ck_value,
                  e_c_value, t_c_value, dis_sup_value, advance_rate_value):
    values = gc(gamma=gamma_value, H=overburden_value, E=e_module,
                nu=nu_value, D=diameter_value, c=cohesion_value,
                phi=phi_value, f_ck=f_ck_value, E_c=e_c_value, t_c=t_c_value,
                dis_sup=dis_sup_value, advance_rate=advance_rate_value)
    if len(values) == 13:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, v1, v1_el, v2, v2_el, v3 = values
    else:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, p7, p8, p9, p10, p11, v1, \
            v1_el, v2, v2_el, v3 = values

    if len(p3_el.y) != 0:
        safety_factor_el = v1_el.val / v2_el.val
    else:
        safety_factor_el = 0

    if len(p3.x) != 0:
        flag = p3.x
        fig = draw(x1=p1.x, y1=p1.y,
                   x2=p2_el.x, y2=p2_el.y,
                   x3=p3_el.x, y3=p3_el.y,
                   safety_factor=safety_factor_el,
                   flag=flag,
                   x4=p4.x, y4=p4.y,
                   x5=p7.x, y5=p7.y,
                   x6=p8.x, y6=p8.y,
                   x7=p9.x, y7=p9.y,
                   x8=p5.x, y8=p5.y,
                   x9=p10.x, y9=p10.y,
                   x10=p11.x, y10=p11.y)
    else:
        fig = draw(x1=p1.x, y1=p1.y,
                   x2=p2_el.x, y2=p2_el.y,
                   x3=p3_el.x, y3=p3_el.y,
                   safety_factor=safety_factor_el,
                   x4=p4.x, y4=p4.y,
                   x8=p5.x, y8=p5.y)

    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True)
