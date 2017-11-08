from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app


layout1 = html.Div(
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


# In[]:
# Helper functions

