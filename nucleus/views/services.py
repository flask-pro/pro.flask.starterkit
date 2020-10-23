from flask import Blueprint
from flask import render_template

from nucleus.models import db

services = Blueprint("services", __name__)


@services.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html.jinja2", template_name="pro.flask.starterkit")


@services.route("/check", methods=["GET"])
def check() -> str:
    db.engine.execute("SELECT version();")
    return "OK"


@services.route("/collapse", methods=["GET"])
def collapse() -> Exception:
    raise Exception("Collapse!")
