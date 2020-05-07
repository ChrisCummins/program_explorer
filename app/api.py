import copy
import os
import subprocess
from functools import lru_cache

# The directory of the root of this project.
_ROOR_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BIN_DIR = os.environ.get("PROGRAM_EXPLORER_BIN", f"{_ROOR_DIR}/bin")
LIB_DIR = os.environ.get("PROGRAM_EXPLORER_LIB", f"{_ROOR_DIR}/lib")

# The binaries used for creating ProgramGraph protocol buffers from compiler
# IRs. Keyed by the IR type.
IR2GRAPH = {
  "LLVM 6.0.0": f"{BIN_DIR}/llvm2graph",
  "XLA HLO": f"{BIN_DIR}/xla2graph",
}

# THe binary used for converting ProgramGraph protocol buffers to graphviz
# dot strings.
GRAPH2DOT = f"{BIN_DIR}/graph2dot"

IR2GRAPH_ENV = copy.copy(os.environ)
IR2GRAPH_ENV["LD_LIBRARY_PATH"] = LIB_DIR


def _BadRequest(message: str, **kwargs):
  d = {"message": message}
  d.update(**kwargs)
  return d, 400


@lru_cache(maxsize=256)
def _Ir2Graph(ir2graph: str, ir: str, version: str):
  p = subprocess.Popen(
    [ir2graph, "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    env=IR2GRAPH_ENV,
  )
  stdout, stderr = p.communicate(ir)
  if p.returncode:
    return _BadRequest("Failed to construct graph from IR", error=stderr)
  return {
    "graph": stdout,
    "message": "OK",
  }


@lru_cache(maxsize=256)
def _Graph2Dot(graph: str):
  p = subprocess.Popen(
    [GRAPH2DOT],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
  )
  stdout, stderr = p.communicate(graph)
  if p.returncode:
    return _BadRequest(
      "Failed to create graphviz from ProGraML graph", error=stderr
    )
  return {
    "dot": stdout,
    "message": "OK",
  }


def Ir2Graph(request):
  """Graph construction API endpoint.

  Args:
    request: A JSON request object.

  Returns:
    A JSON response, optionally with an error code.
  """
  ir: str = request.pop("ir")
  if not ir:
    return _BadRequest("Required argument missing: ir")
  ir_type: str = request.pop("type")
  if not ir_type:
    return _BadRequest(
      f'Required argument missing: type. Expected one of: {", ".join(sorted(IR2GRAPH.keys()))}'
    )

  version: str = request.pop("version")
  if not version:
    return _BadRequest("Required argument missing: version")

  if request:
    return _BadRequest(f"Unknown arguments: {', '.join(sorted(request))}")

  if version != "ProGraML 2020.05.06":
    return _BadRequest(f"Unknown version: {version}")

  ir2graph = IR2GRAPH.get(ir_type)
  if not ir2graph:
    return _BadRequest(
      f"Unknown ir: {ir_type}. Expected one of: {', '.join(sorted(IR2GRAPH.keys()))}"
    )

  return _Ir2Graph(ir2graph, ir, version)


def Graph2Dot(request):
  """Graphviz dot construction API endpoint.

  Args:
    request: A JSON request object.

  Returns:
    A JSON response, optionally with an error code.
  """
  graph = request.get("graph")
  if not graph:
    return _BadRequest("Required argument missing: graph")

  return _Graph2Dot(graph)
