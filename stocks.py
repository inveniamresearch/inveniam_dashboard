import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
from pandas_datareader.data import DataReader
import time

from app import app

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

df_symbol = pd.read_csv('tickers.csv')

layout = html.Div([
    html.Div([
        html.H2('Financial Analytics',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '10px',
                       'margin-bottom': '0'
                       }),
        html.Img(src="https://cdn.rawgit.com/plotly/design-assets/a8c0b6972563dfa3e8e7b5d7454d4909fa9db21b/logo/dash/images/dash-logo-by-plotly-stripe.png?token=ARkbwzp9Cq3SoAp8SBfsMVVfotVrJJUxks5ZW_jVwA%3D%3D",
                style={
                    'height': '100px',
                    'float': 'right'
                },
        ),
    ]),
    html.Div([
        dcc.Dropdown(
            id='stock-ticker-input',
            options=[{'label': s[0], 'value': s[1]}
                     for s in zip(df_symbol.Company, df_symbol.Symbol)],
            value=['YHOO', 'GOOGL'],
            multi=True
        ),],style={"padding":"10px"}),
        html.Div(id='graphs',style={"padding":"10px"})
],)

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(tickers):
    graphs = []
    for i, ticker in enumerate(tickers):
        try:
            df = DataReader(ticker, 'google',
                            dt.datetime(2017, 1, 1),
                            dt.datetime.now())
        except:
            graphs.append(html.H3(
                'Data is not available for {}'.format(ticker),
                style={'marginTop': 20, 'marginBottom': 20}
            ))
            continue

        candlestick = {
            'x': df.index,
            'open': df['Open'],
            'high': df['High'],
            'low': df['Low'],
            'close': df['Close'],
            'type': 'candlestick',
            'name': ticker,
            'legendgroup': ticker,
            'increasing': {'line': {'color': colorscale[0]}},
            'decreasing': {'line': {'color': colorscale[1]}}
        }
        bb_bands = bbands(df.Close)
        bollinger_traces = [{
            'x': df.index, 'y': y,
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
            'hoverinfo': 'none',
            'legendgroup': ticker,
            'showlegend': True if i == 0 else False,
            'name': '{} - bollinger bands'.format(ticker)
        } for i, y in enumerate(bb_bands)]
        graphs.append(dcc.Graph(
            id=ticker,
            figure={
                'data': [candlestick] + bollinger_traces,
                'layout': {
                    'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                    'legend': {'x': 0}
                }
            }
        ))

    return graphs

