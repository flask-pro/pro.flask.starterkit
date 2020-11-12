from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics.for_app_factory()
db = SQLAlchemy()


def register_extensions(app: Flask) -> Flask:
    metrics.init_app(app)
    db.init_app(app)
    return app
