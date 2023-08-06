# -*- coding: utf-8 -*-
import os
import re

from flask import Flask

from clustermgr.extensions import db, csrf, migrate, wlogger


def init_celery(app, celery):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


def create_app():
    app = Flask(__name__)

    # Configure the flask application
    cfg = "clustermgr.config.DevelopmentConfig"  # default
    app_mode = os.environ.get("APP_MODE")        # override using env var
    if app_mode == "prod":
        cfg = "clustermgr.config.ProductionConfig"
    elif app_mode == "test":
        cfg = "clustermgr.config.TestConfig"
    app.config.from_object(cfg)
    app.instance_path = app.config["APP_INSTANCE_DIR"]
    # allow custom config
    app.config.from_pyfile(
        os.path.join(app.instance_path, "config.py"),
        silent=True,
    )

    # Initialize the extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(os.path.dirname(__file__),
                                                     "migrations"))
    wlogger.init_app(app)

    # setup the instance's working directories
    if not os.path.isdir(app.config['SCHEMA_DIR']):
        os.makedirs(app.config['SCHEMA_DIR'])
    if not os.path.isdir(app.config['SLAPDCONF_DIR']):
        os.makedirs(app.config['SLAPDCONF_DIR'])
    if not os.path.isdir(app.config['LDIF_DIR']):
        os.makedirs(app.config['LDIF_DIR'])
    if not os.path.isdir(app.config['CERTS_DIR']):
        os.makedirs(app.config['CERTS_DIR'])
    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    # register blueprints
    from clustermgr.views.index import index
    from clustermgr.views.server import server_view
    from clustermgr.views.cluster import cluster
    from clustermgr.views.logserver import logserver
    from clustermgr.views.cache import cache_mgr
    app.register_blueprint(index, url_prefix="")
    app.register_blueprint(server_view, url_prefix="/server")
    app.register_blueprint(cluster, url_prefix="/cluster")
    app.register_blueprint(logserver, url_prefix="/logging_server")
    app.register_blueprint(cache_mgr, url_prefix="/cache")

    @app.context_processor
    def hash_processor():
        def hashed_url(filepath):
            directory, filename = filepath.rsplit('/')
            name, extension = filename.rsplit(".")
            folder = os.path.join(app.root_path, 'static', directory)
            files = os.listdir(folder)
            for f in files:
                regex = name+"\.[a-z0-9]+\."+extension
                if re.match(regex, f):
                    return os.path.join('/static', directory, f)
            return os.path.join('/static', filepath)
        return dict(hashed_url=hashed_url)

    return app
