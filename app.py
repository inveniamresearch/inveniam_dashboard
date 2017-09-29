from flask import Flask
import dash
import os

server = Flask(__name__)

server.secret_key = os.environ.get('secret_key', 'secret')
#print(server.secret_key)
app = dash.Dash(__name__, server=server,csrf_protect=False)
app.config.supress_callback_exceptions = True