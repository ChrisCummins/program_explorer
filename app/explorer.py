import flask

from app import api
from app import explorer


# The default IR to display.
DEFAULT_IR = """\
int Fib(int x) {
    switch(x) {
        case 0:
            return 0;
        case 1:
            return 1;
        default:
            return Fib(x - 1) + Fib(x - 2);
  }
}
"""

ENDPOINTS = api.EnumerateIr2GraphJson()


def Explorer(urls):
  data = {
    "ir": DEFAULT_IR,
    "endpoints": ENDPOINTS,
    "defaults": {
      "ir": DEFAULT_IR,
      "lang": "clang",
      "version": "default",
      "programl_version": "default",
    },
  }
  urls["highlight_js"] = flask.url_for("static", filename="highlight.pack.js")
  urls["explorer_js"] = flask.url_for("static", filename="explorer.js")
  return flask.render_template("explorer.html", data=data, urls=urls)
