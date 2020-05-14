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


@app.route("/api/v1/ir2graph")
def enumerate_ir2graph():
  if request.content_type == "application/json":
    return api.EnumerateIr2GraphJson()
  else:
    return api.EnumerateIr2Graph(prefix=request.url_rule)


@app.route(
  "/api/v1/ir2graph/<lang_version>",
  methods=["POST"],
  defaults={"programl_version": "2020.05.06"},
)
@app.route(
  "/api/v1/ir2graph<programl_version>/<lang_version>", methods=["POST"]
)
def ir2graph(programl_version: str, lang_version: str):
  if ":" in lang_version:
    lang, version = lang_version.split(":")
  else:
    lang, version = lang_version, "default"
  ir = request.get_data().decode("utf-8")
  if programl_version[0] == ":":
    programl_version = programl_version[1:]
  return api.Ir2Graph(programl_version, lang, version, ir)


@app.route("/api/v1/graph2dot", methods=["POST"])
def graph2dot():
  graph = request.get_data().decode("utf-8")
  return api.Graph2Dot(graph)
