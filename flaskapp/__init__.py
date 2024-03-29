import os 

from flask import Flask 

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='qwerty1',
        DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    from . import main
    app.register_blueprint(main.bp)
    
    @app.route('/')
    def hello():
        return 'hell world'

    return app

    