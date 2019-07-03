# -*- coding: utf-8 -*-
import plotly.graph_objs as go


def draw(x1, y1,
         x2, y2,
         x3, y3,
         safety_factor,
         flag=None,
         x4=None, y4=None,
         x5=None, y5=None,
         x6=None, y6=None,
         x7=None, y7=None,
         x8=None, y8=None,
         x9=None, y9=None,
         x10=None, y10=None,
         x11=None, y11=None):
    trace0 = go.Scatter(
        x=x1,
        y=y1,
        mode='lines',
        name='Ground curve',
        line=dict(
            color='blue'
        ),
        xaxis='x1',
        yaxis='y1'
    )

    trace1 = go.Scatter(
        x=x2,
        y=y2,
        mode='lines',
        name='Support (LE)',
        line=dict(
            color='red'
        ),
        xaxis='x1',
        yaxis='y1'
    )

    trace2 = go.Scatter(
        x=x3,
        y=y3,
        mode='markers',
        name=f'F.S.={safety_factor:0.2f}',
        marker=dict(
            size=7,
            color='green'
        ),
        xaxis='x1',
        yaxis='y1'
    )

    trace3 = go.Scatter(
        x=x4,
        y=y4,
        mode='lines',
        name='Org. LDP',
        line=dict(
            color='blue',
            width=1.5,
            dash='dashdot'
        ),
        xaxis='x1',
        yaxis='y2'
    )

    data = [trace0, trace1, trace2, trace3]

    shapes = list()  # append the vertical lines later

    if flag is not None:
        for index, item in enumerate(x6):
            if index % 30 == 0:
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
                    name='Diff. p_i',
                    opacity=0.4,
                    xaxis='x1',
                    yaxis='y2'
                )
                data.append(trace5)

        trace5 = go.Scatter(
            x=x6[-1],
            y=y6,
            mode='lines',
            line=dict(
                color='green',
                width=1.5,
                dash='dashdot'
            ),
            visible=True,
            showlegend=False,
            legendgroup="group",
            hoverinfo='none',
            name='Diff. p_i',
            opacity=1,
            xaxis='x1',
            yaxis='y2'
        )
        data.append(trace5)

        # vertical lines
        for i in (x2[0], x3[0]):
            shapes.append({'type': 'line',
                           'xref': 'x1',
                           'yref': 'y2',
                           'x0': i,
                           'y0': 0,
                           'x1': i,
                           'y1': 80,
                           'line': {
                               'color': 'red',
                               'width': 1.5,
                               'dash': 'dashdot'},
                           'opacity' : 0.6
                           })

        trace6 = go.Scatter(
            x=x7,
            y=y7,
            mode='lines',
            name='New LDP',
            line=dict(
                color='red',
                width=2
            ),
            xaxis='x1',
            yaxis='y2'
        )
        data.append(trace6)

    trace7 = go.Scatter(
        x=x8,
        y=y8,
        mode='lines',
        name='Support (NL)',
        line=dict(
            color='green'
        ),
        xaxis='x2',
        yaxis='y3',
        # showlegend=False,
    )

    trace8 = go.Scatter(
        x=x9,
        y=y9,
        mode='lines',
        name='Flow Rate',
        line=dict(
            color='red'
        ),
        xaxis='x2',
        yaxis='y4'
    )

    trace9 = go.Scatter(
        x=x10,
        y=y10,
        mode='lines',
        name='Support (NL)',
        line=dict(
            color='green'
        ),
        xaxis='x2',
        yaxis='y4',
        showlegend=False,
        # hoverinfo='x+y'
    )

    trace10 = go.Scatter(
        x=x11,
        y=y11,
        mode='markers',
        name='Critical Point',
        line=dict(
            color='brown'
        ),
        xaxis='x1',
        yaxis='y1',
        showlegend=True,
        opacity=0.5
    )

    data.extend([trace7, trace8, trace9, trace10])

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
        width=1200,
        height=800,
        xaxis=dict(
            rangemode='normal',
            title='Tunnel Wall Displacement [m]',
            range=[0, max(x1)],
            tickformat='.3f',
            domain=[0, 0.47],
            anchor='y2'
        ),
        yaxis=dict(
            scaleratio=0.1,
            tickformat='.2f',
            title='Support Pressure [MPa]',
            titlefont=dict(size=14),
            range=[0, max(y1)],
            domain=[0.55, 1]
        ),
        xaxis2=dict(
            title='Time [days]',
            tickformat='.2f',
            domain=[0.55, 1],
            anchor='y4'
        ),
        yaxis2=dict(
            title='Distance from Tunnel Face [m]',
            tickformat='.2f',
            anchor='x1',
            range=[80, -25],
            domain=[0, 0.50]
        ),
        yaxis3=dict(
            title='Support Pressure [MPa]',
            tickformat='.2f',
            range = [0, max(y1)],
            domain=[0.55, 1],
            anchor='x2'
        ),
        yaxis4=dict(
            title='Stress SpC [MPa]',
            tickformat='.2f',
            domain=[0, 0.50],
            anchor='x2',
            rangemode='nonnegative'
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
        ),
        shapes=shapes
    )

    fig = go.Figure(data=data, layout=layout)

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
               x7=p9.x, y7=p9.y,
               x8=p5.x, y8=p5.y,
               x9=p10.x, y9=p10.y,
               x10=p11.x, y10=p11.y)
    plot(fig, filename='ground_curve_basic.html')
