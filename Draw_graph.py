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
         x10=None, y10=None):
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
        name='SCL (NL)',
        line=dict(
            color='red'
        ),
        xaxis='x2',
        yaxis='y3'
    )

    trace8 = go.Scatter(
        x=x9,
        y=y9,
        mode='lines',
        name='Flow Rate',
        line=dict(
            color='blue'
        ),
        xaxis='x2',
        yaxis='y4'
    )

    trace9 = go.Scatter(
        x=x10,
        y=y10,
        mode='lines',
        name='Sigma (NL)',
        line=dict(
            color='red'
        ),
        xaxis='x2',
        yaxis='y4'
    )

    data.extend([trace7, trace8, trace9])

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
            tickformat='d',
            domain=[0.55, 1],
            anchor='y4'
        ),
        yaxis2=dict(
            title='Distance from Tunnel Face [m]',
            tickformat='d',
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
