from flask import Flask, session, render_template, request_started
from werkzeug import SharedDataMiddleware
import os

# create our application
app = Flask(__name__)

# Config
if app.config['DEBUG']:
    app.config.from_object('flask_application.config.DevelopmentConfig')
    app.logger.info("Config: Development")
else:
    app.config.from_object('flask_application.config.ProductionConfig')
    app.logger.info("Config: Production")

# Source: http://www.jeffff.com/serving-media-in-the-flask-local-dev-server:w
def serve_static(sender):
     if app.config['DEBUG']:
         app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                        {'/':os.path.join(os.path.dirname(__file__), 'static') })

request_started.connect(serve_static, app)


@app.before_request
def before_request():
       session["debug"] = app.debug

@app.after_request
def after_request(response):
    return response

@app.context_processor
def inject_site_defaults():
        return dict(site_title="<YOUR SITE TITLE HERE>")

@app.route('/')
def page_home():
    return render_template('page_t_home.html', page_title="Home")
