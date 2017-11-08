from flask import Flask
import dash
import os
import colorlover as cl
import datetime as dt
import pandas as pd
from pandas_datareader.data import DataReader
import time
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os

server = Flask(__name__)

server.secret_key = os.environ.get('secret_key', 'secret')
#print(server.secret_key)
app = dash.Dash(__name__, server=server,csrf_protect=False)
app.config.supress_callback_exceptions = True


app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css'})  # noqa: E501
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
    })


app.layout = html.Div([
				dcc.Location(id='url',refresh=True),
				#dcc.Location(id='url'),
				html.Div([
					html.Table([
						html.Tr([
							html.Td([
								html.Div([
										html.Img(
                    					src="https://s3.amazonaws.com/inveniamlogo/blue_circle_logo.png",
		                    			style={
						                       	'height': '60px',
						                        'float': 'none',
						                        'width':'75%'
		                    				},)],style={"background-color":"#F1F5F8","width":"85%"}),
                			],style={"width":"45%"}),
							html.Td([dcc.Link('Oil and Gas Well Data',href='/oil_and_gas')]),
							html.Td([dcc.Link('Financial Analytics',href='/stocks')]),
							html.Td([dcc.Link('Research Reports',href='/reports')]),
							html.Td([dcc.Link('Contact Us',href='/contactUs')]),
							]),],style={'width':'100%'})],
												style={'height': '64px',
												'font': 'normal normal 600 1em/4em Arial,sans-serif',
												'text-decoration': 'none',
    											'color': 'white',
											    'background-color': '#00A3DA',
    											'display':'block',
    											'width':'100%',
    											'padding-left':'5px'
												 #'background-color': 'black'
												 }),
				html.Div([
					],id="app_info_content"),

			])


app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

df_symbol = pd.read_csv('tickers.csv')

stock_layout = html.Div([
    html.Div([
        html.H2('Financial Analytics',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '10px',
                       'margin-bottom': '5px',
                       'margin-left': '10px',
                       }),
        html.Img(src="https://cdn.rawgit.com/plotly/design-assets/a8c0b6972563dfa3e8e7b5d7454d4909fa9db21b/logo/dash/images/dash-logo-by-plotly-stripe.png?token=ARkbwzp9Cq3SoAp8SBfsMVVfotVrJJUxks5ZW_jVwA%3D%3D",
                style={
                    'height': '100px',
                },
        ),
    ]),
    html.Div([
        dcc.Dropdown(
            id='stock-ticker-input',
            options=[{'label': s[0], 'value': s[1]}
                     for s in zip(df_symbol.Company, df_symbol.Symbol)],
            value=['PES', 'EOG'],
            multi=True
        ),],style={"padding":"10px"}),
        html.Div(id='graphs',style={"padding":"10px"})
])

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
                    'margin': {'b': 0, 'r': 0, 'l': 50, 't': 0},
                    'legend': {'x': 0}
                }
            }
        ))

    return graphs


contactUs_layout = html.Div(
    [        
        html.Div(
            [
                html.H1(
                    'Contact Us'
                ),
            ],style={"padding":"10px"}
        ),
        html.Div(
            [
                html.Table([
                    html.Tr([
                        html.Td([
                        	html.Div([
                        		html.Div([
                        				html.H6("Please feel free to reach out directly to us at info@inveniamfunds.com or use the submission form directly to the right of this page.  Alternatively, you can write directly to us at the address below. We look forward to hearing from you.")
                        			],style={'width':"100%","padding":"20px"}),
                        		html.Div([
                        			html.Div([
                        					html.P("Name"),
                        					dcc.Input(
                        						placeholder="Name",
                        						type="text",
                        						value="",
                        						id="contactUs_Name",
                        						style={'width': '80%'},
                        						className="form-control"),

                        				],style={'padding':"15px"}),
                        			html.Div([
                        					html.P("Email"),
                        					dcc.Input(
                        						placeholder="Email",
                        						type="text",
                        						value="",
                        						id="contactUs_Email",
                        						style={'width': '80%'},
                        						className="form-control"),

                        				],style={'padding':"15px"}),
                        			html.Div([
                        					html.P("Message"),
                        					dcc.Textarea(
                        						placeholder="Message",
                        						value="",
                        						id="contactUs_Message",
                        						style={'width': '80%'},
                        						className="form-control"),

                        				],style={'padding':"15px"}),
                        				html.Div([
                        					html.Button(
                        						"Submit",
                           						id="contactUs_submit",
                           						className="btn btn-primary"
                        						),
                        				],style={'padding':"15px","align":"left"}),

                        			],style={'width':"100%"},className="form-group")	
                        		])
                            ,],style={"width":"70%"}),
                        html.Td([
                        	html.Div([
                        			html.Div([
                        				html.P([
                        					html.B("Houston"),
                        					]),
                        				html.P([
                        					"1322 Space Park Drive Suite A155 Houston, TX 77058-3400",
                        					]),
                        				]),
                        			html.Div([
                        				html.P([
                        					html.B("Phone:"),
                        					]),
                        				html.P([
                        					"+1 844-882-7437",
                        					]),
                        				]),
                        			html.Div([
                        				html.P([
                        					html.B("Email:"),
                        					]),
                        				html.P([
                        					"info@inveniamfunds.com",
                        					]),
                        				]),
                        			html.Div([
                        				html.P([
                        					html.B("Business Hours:"),
                        					]),
                        				html.P([
                        					"Weekdays: 9am to 5pm",
                        					]),
                        				]),
                        			html.Div([
                        				html.P([
                        					html.B("Web:"),
                        					]),
                        				html.P([
                        					"http://inveniamfunds.com",
                        					]),
                        				]),

                        		],style={"width":"100%"}),
                        	],style={"width":"30%","vertical-align":"top"}),
                        ]),],style={"width":"100%"}),
            ]),
                  ],style={"width":"100%",'padding':"40px"})


#app.layout = serve_layout

oil_and_gas_layout = html.Iframe(src="http://54.88.94.245:83/dash/gallery/new-york-oil-and-gas/",style={
    "frameborder":"0",
    "width":'100%',
    "height":"1500px",
    "scrolling":"no"
    })


reports_layout = html.Iframe(src="http://54.88.94.245:81/dash/gallery/goldman-sachs-report/",style={
    "frameborder":"0",
    "width":'100%',
    "height":"2350px",
    "scrolling":"no",
    })

@app.callback(dash.dependencies.Output('app_info_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	if pathname=='/oil_and_gas':
		print(pathname)
		return oil_and_gas_layout
	elif pathname=='/stocks':
		return stock_layout
	elif pathname=="/contactUs":
		return contactUs_layout
	elif pathname=="/reports":
		return reports_layout
	else:
		return oil_and_gas_layout

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)