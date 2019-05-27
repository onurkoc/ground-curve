# -*- coding: utf-8 -*-
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools


def draw(x1, y1,
         x2, y2,
         x3, y3,
         safety_factor,
         flag=None,
         x4=None, y4=None,
         x5=None, y5=None,
         x6=None, y6=None,
         x7=None, y7=None):
    trace0 = go.Scatter(
        x=x1,
        y=y1,
        mode='lines',
        name='Ground curve',
        line=dict(
            color='blue'
        ),
        hoverinfo='none',
    )

    trace1 = go.Scatter(
        x=x2,
        y=y2,
        mode='lines',
        name='Support',
        line=dict(
            color='green'
        ),
        hoverinfo='none'
    )

    trace2 = go.Scatter(
        x=x3,
        y=y3,
        mode='markers',
        name=f'F.S.={safety_factor:0.2f}',
        marker=dict(
            size=5,
            color='red'
        )
    )

    fig = tools.make_subplots(rows=2, cols=1,
                              shared_xaxes=True,
                              shared_yaxes=False,
                              vertical_spacing=0.07,
                              # subplot_titles=('Ground Reaction Curve',
                              #                 'Displacement Curve')
                              )

    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)

    trace3 = go.Scatter(
        x=x4,
        y=y4,
        mode='lines',
        name='Org. LDP',
        line=dict(
            color='blue',
            width=1.5,
            dash='dashdot'
        )
    )

    fig.append_trace(trace3, 2, 1)

    if flag is not None:
        trace4 = go.Scatter(
            x=x5,
            y=y5,
            mode='lines',
            line=dict(
                color='green',
                width=1.5,
                dash='dashdot'
            ),
            name='Equil. LDP'
        )
        fig.append_trace(trace4, 2, 1)
        for index, item in enumerate(x6):
            if index % 10 == 0:
                trace5 = go.Scatter(
                    x=item,
                    y=y6,
                    mode='lines',
                    line=dict(
                        color='gray',
                        width=1,
                        dash='dashdot'
                    ),
                    visible=True,  # 'legendonly' displays only in legend
                    showlegend=False,
                    legendgroup="group",
                    hoverinfo='none',
                    name='Diff. p_i'
                )
                fig.append_trace(trace5, 2, 1)

        trace6 = go.Scatter(
            x=x7,
            y=y7,
            mode='lines',
            name='New LDP',
            line=dict(
                color='red'
            )
        )
        fig.append_trace(trace6, 2, 1)

    layout = go.Layout(
        plot_bgcolor='#f9f7f7',
        showlegend=True,
        margin=dict(
            l=75,
            r=50,
            b=50,
            t=50,
            pad=4
        ),
        titlefont=dict(
            size=20,
        ),
        hovermode='closest',
        autosize=True,
        width=800,
        height=800,
        xaxis=dict(
            rangemode='normal',
            titlefont=dict(size=14),
        ),
        yaxis=dict(
            scaleratio=0.1,
            tickformat='.2f',
            title='Support Pressure [MPa]',
            titlefont=dict(size=14),
        ),
        xaxis2=dict(
            side='top',
            title='Tunnel Wall Displacement [m]',
        ),
        yaxis2=dict(
            autorange='reversed',
            title='Distance from Tunnel Face [m]',
        ),
        legend=dict(
            traceorder='normal',
            font=dict(
                family='arial',
                size=12,
                color='#000'
            ),
            bgcolor='#E2E2E2',
            bordercolor='#FFFFFF',
            borderwidth=1.5
        )
    )

    fig['layout'].update(layout)

    return fig


if __name__ == '__main__':
    from plotly.offline import plot
    from Ground_Curve import ground_curve as gc
    values = gc()
    if len(values) == 13:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, v1, v1_el, v2, v2_el, v3 = values
    else:
        p1, p2, p2_el, p3, p3_el, p4, p5, p6, p7, p8, p9, p10, p11, v1, \
        v1_el, v2, v2_el, v3 = values
    flag = p3.x
    if len(p3_el.y) != 0:
        safety_factor_el = v1_el.val / v2_el.val
    else:
        safety_factor_el = 0
    fig = draw(x1=p1.x, y1=p1.y,
               x2=p2_el.x, y2=p2_el.y,
               x3=p3_el.x, y3=p3_el.y,
               safety_factor=safety_factor_el,
               flag=flag,
               x4=p4.x, y4=p4.y,
               x5=p7.x, y5=p7.y,
               x6=p8.x, y6=p8.y,
               x7=p9.x, y7=p9.y)
    plot(fig, filename='ground_curve_basic.html')
