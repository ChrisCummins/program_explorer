import time

import flask
from flask import request

from app import api
from app import app
from app.about import About
from app.explorer import Explorer


def _BaseUrls():
  return {
    "cache_tag": int(time.time()),
    "bootstrap_css": flask.url_for("static", filename="bootstrap.css"),
  }


@app.route("/")
@app.route("/index")
def index():
  return Explorer(urls=_BaseUrls())


@app.route("/about")
def about():
  return About(urls=_BaseUrls())


# API endpoints.


@app.route("/api/v1/ir2graph", methods=["POST"])
def ir2graph():
  return api.Ir2Graph(request.json)


@app.route("/api/v1/graph2dot", methods=["POST"])
def graph2dot():
  return api.Graph2Dot(request.json)
