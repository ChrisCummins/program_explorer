import flask

from app import explorer


# The default IR to display.
DEFAULT_IR = """\
source_filename = "example.c"

define i32 @Fib(i32) local_unnamed_addr #0 {
  switch i32 %0, label %3 [
    i32 0, label %9
    i32 1, label %2
  ]

; <label>:2:
  br label %9

; <label>:3:
  %4 = add nsw i32 %0, -1
  %5 = tail call i32 @Fib(i32 %4)
  %6 = add nsw i32 %0, -2
  %7 = tail call i32 @Fib(i32 %6)
  %8 = add nsw i32 %7, %5
  ret i32 %8

; <label>:9:
  %10 = phi i32 [ 1, %2 ], [ %0, %1 ]
  ret i32 %10
}
"""


def Explorer(urls):
  data = {
    "ir": DEFAULT_IR,
  }
  urls["highlight_js"] = flask.url_for("static", filename="highlight.pack.js")
  urls["explorer_js"] = flask.url_for("static", filename="explorer.js")
  return flask.render_template("explorer.html", data=data, urls=urls)
