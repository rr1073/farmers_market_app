import os

from flask import Flask

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
                SECRET_KEY='secret',
                DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
            )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.sqlite')
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db, extensions, market
    db.init_app(app)

    app.register_blueprint(market.bp, url_prefix='/market')
    app.add_url_rule('/', endpoint='market.index')

    #Flask-SQLAlchemy
    extensions.dbalch.init_app(app)

    return app
