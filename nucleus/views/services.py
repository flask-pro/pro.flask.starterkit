from flask import render_template

from nucleus.models import db


def registration_service_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html.jinja2', template_name='pro.flask.starterkit')

    @app.route('/check', methods=['GET'])
    def check():
        db.engine.execute('SELECT version();')
        return 'OK'

    @app.route('/collapse', methods=['GET'])
    def collapse():
        raise Exception('Collapse!')

    return app
