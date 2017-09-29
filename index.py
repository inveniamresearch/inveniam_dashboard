import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os
from app import app
import oil_and_gas,reports,stocks,contactUs

app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css'})  # noqa: E501
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
    })



app.layout = html.Div([
				#dcc.Location(id='url'),
				html.Div([
					html.Img(
                    			src="https://s3.amazonaws.com/inveniamlogo/logo.png",
                    			style={
				                        'height': '300px',
				                        'float': 'none',
				                        'width':'100%'
                    				},
                			)]),
				html.Div([
					html.Table([
						html.Tr([
							dcc.Location(id='url'),
							html.Td([dcc.Link('Oil and Gas Well Data',href='/oil_and_gas')]),
							html.Td([dcc.Link('Financial Analytics',href='/stocks')]),
							html.Td([dcc.Link('Research Reports',href='/apps/reports')]),
							html.Td([dcc.Link('Contact Us',href='/contactUs')]),
							]),],style={'width':'100%'})],
												style={'height': '60px',
												'font': 'normal normal 600 1em/4em Arial,sans-serif',
												'text-decoration': 'none',
    											'color': 'white',
											    'background-color': '#00A3DA',
    											'display':'block',
    											'width':'100%',
    											'padding-left':'5px',
												 #'background-color': 'black'
												 }),
				html.Div([
					],id="app_info_content"),

			])

@app.callback(Output('app_info_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
	if pathname=='/oil_and_gas':
		print(pathname)
		return oil_and_gas.layout
	elif pathname=='/stocks':
		return stocks.layout
	elif pathname=="/contactUs":
		return contactUs.layout
	else:
		return oil_and_gas.layout

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)