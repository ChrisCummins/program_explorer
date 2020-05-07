import flask


def About(urls):
  return flask.render_template("about.html", urls=urls)
