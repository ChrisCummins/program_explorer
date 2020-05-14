import copy
import os
import pathlib
import subprocess
from functools import lru_cache

# The directory of the root of this project.
_ROOR_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BIN_DIR = pathlib.Path(
  os.environ.get("PROGRAM_EXPLORER_BIN", f"{_ROOR_DIR}/bin")
)
LIB_DIR = pathlib.Path(
  os.environ.get("PROGRAM_EXPLORER_LIB", f"{_ROOR_DIR}/lib")
)

# THe binary used for converting ProgramGraph protocol buffers to graphviz
# dot strings.
GRAPH2DOT = f"{BIN_DIR}/graph2dot"

IR2GRAPH_ENV = copy.copy(os.environ)
IR2GRAPH_ENV["LD_LIBRARY_PATH"] = str(LIB_DIR)


@lru_cache(maxsize=256)
def _Ir2Graph(ir2graph: str, ir: str):
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
    return stderr, 400
  return stdout


# Dynamic dispatch table for <language, version, programl_version> translation to
# binary path.
IR2GRAPH = {}
for lang in (BIN_DIR / "ir2graph").iterdir():
  if lang.name not in IR2GRAPH:
    IR2GRAPH[lang.name] = {}
  for version in lang.iterdir():
    if version.name not in IR2GRAPH[lang.name]:
      IR2GRAPH[lang.name][version.name] = {}
    for programl_version in version.iterdir():
      IR2GRAPH[lang.name][version.name][
        programl_version.name
      ] = programl_version.absolute()


def EnumerateIr2Graph(prefix: str = ""):
  endpoints = []
  for lang, versions in sorted(IR2GRAPH.items()):
    endpoints.append(f"{prefix}/{lang}")
    for version, programl_versions in sorted(versions.items()):
      endpoints.append(f"{prefix}/{lang}:{version}")
      for programl_version in sorted(programl_versions):
        endpoints.append(f"{prefix}:{programl_version}/{lang}:{version}")
  return "\n".join(endpoints) + "\n"


def EnumerateIr2GraphJson():
  endpoints = {}
  for lang, versions in IR2GRAPH.items():
    endpoints[lang] = {}
    for version, programl_versions in versions.items():
      endpoints[lang][version] = []
      for programl_version in programl_versions:
        endpoints[lang][version].append(programl_version)
  return endpoints


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
    return stderr, 400
  return stdout


def Ir2Graph(programl_version: str, lang: str, version: str, ir: bytes):
  """Graph construction API endpoint.

  Args:
    lang: The language to convert.

  Returns:
    A JSON response, optionally with an error code.
  """
  if not lang in IR2GRAPH:
    return "Unknown language", 400
  if version not in IR2GRAPH[lang]:
    return (
      f"Unsupported language version: {version}. Expected one of: {', '.join(sorted(IR2GRAPH[lang]))}",
      400,
    )
  if programl_version not in IR2GRAPH[lang][version]:
    return (
      f"Unsupported ProGraML version: {version}. Expected one of: {', '.join(sorted(IR2GRAPH[lang][version]))}",
      400,
    )
  return _Ir2Graph(IR2GRAPH[lang][version][programl_version], ir)


def Graph2Dot(graph: str):
  """Graphviz dot construction API endpoint.

  Args:
    request: A JSON request object.

  Returns:
    A JSON response, optionally with an error code.
  """
  return _Graph2Dot(graph)
