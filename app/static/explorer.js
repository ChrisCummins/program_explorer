hljs.initHighlightingOnLoad();

var editor = ace.edit("ir-editor", {
  autoScrollEditorIntoView: true,
  maxLines: 60,
  minLines: 60
});

// Cache the current state of IR to compare against in event callbacks.
var currentIrState = {
  "ir": null,
  "lang": null,
  "version": null,
  "programl_version": null,
};

// A map from IR type names to file suffixes, used to generate the file extension
// for the "Download" button.
var lang2suffix = {
  "llvm": ".ll",
  "xla": ".pbtxt",
}

// The dot string for the currently rendered graph.
var dot = '';

var DownloadText = function(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

var EncodeQueryData = function(data) {
  const ret = [];
  for (let d in data)
    ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
  return ret.join('&');
}

/**
 * The complemeent of SetAppState().
 */
var AppStateToUri = function() {
  return EncodeQueryData({
    i: currentIrState['ir'],
    t: $('#ir-type').children("option:selected").val(),
    p: $('#programl-version').children("option:selected").val(),
    g: $('#graph-select').children("option:selected").val(),
  });
}

/**
 * The complemeent of AppStateToUri().
 */
var SetAppState = function(uri) {
  state = DecodeQueryData(uri);
  editor.setValue(state.i);
  $('#ir-type').val(state.t);
  OnLangChange(false);
  $('#programl-version').val(state.p);
  $('#graph-select').val(state.g);
}

var DecodeQueryData = function(uri) {
  var dictionary = {};
  if (uri.indexOf('#') === 0) {
    uri = uri.substr(1);
  }

  var parts = uri.split('&');
  for (var i = 0; i < parts.length; i++) {
    var p = parts[i];
    var keyValuePair = p.split('=');

    var key = keyValuePair[0];
    var value = keyValuePair[1];

    value = decodeURIComponent(value);
    // value = value.replace(/\+/g, ' ');

    dictionary[key] = value;
  }

  return dictionary;
}

var OnLangChange = function(resetDefaultIr) {
  var ir_type = $('#ir-type').children("option:selected");

  var lang = $('#ir-type').children("option:selected").attr("data-lang");
  var version = $('#ir-type').children("option:selected").attr("data-version");

  // We have switched from one IR language to another, e.g.
  // from LLVM to XLA, so reset the IR text to the language
  // default.
  if (resetDefaultIr && lang != currentIrState['lang']) {
    // Set the defualt IR to the current text so that a user can recover their text.
    default_irs[currentIrState['lang']] = editor.getValue();
    editor.setValue(default_irs[lang]);
  }

  // Reset ProGraML version list.
  var programl_version_selector = $('#programl-version');
  programl_version_selector.empty();
  ir2graph_api_endpoints[lang][version].forEach(function(item, index) {
    var selected = item == "default" ? " selected " : ""
    programl_version_selector.append("<option data-programl-version=\"" + item + "\"" + selected + ">" + item + "</option>");
  });
}

var OnIrChange = function() {
  // DOM elements.
  var pbtxt_loading = $('#pbtxt-loading');
  var graph = $('#graph');
  var graph_loading = $('#graph-loading');
  var ir_type = $('#ir-type').children("option:selected");

  var lang = ir_type.attr("data-lang");
  var ir_version = ir_type.attr("data-version");
  var programl_version = $('#programl-version').children("option:selected").attr("data-programl-version");
  var pbtxt = $('#pbtxt');
  var pbtxt_error = $('#pbtxt-error');
  var pbtxt_error_msg = $('#pbtxt-error .message');
  var graph_error = $('#graph-error');

  var ir = editor.getValue();

  // Chekc if the state of the IR has changed, so that we know it needs
  // re-rendering.
  var newIrState = {
    "ir": ir,
    "lang": lang,
    "version": ir_version,
    "programl_version": programl_version,
  }
  if (currentIrState['lang'] === newIrState['lang'] &&
    currentIrState['version'] === newIrState['version'] &&
    currentIrState['programl_version'] === newIrState['programl_version'] &&
    currentIrState['ir'] === newIrState['ir']) {
    return;
  }
  currentIrState = newIrState;

  // Hide other columns.
  pbtxt_error.hide();
  pbtxt.hide();
  graph.hide();
  pbtxt_error.hide();
  graph_error.hide();

  if (!ir) {
    return;
  }

  pbtxt_loading.show();
  graph_loading.show();

  $.ajax({
    type: "POST",
    url: "/api/v1/ir2graph:" + programl_version + "/" + newIrState['lang'] + ":" + newIrState['version'],
    data: ir,
    contentType: "text/plain",
    success: function(response, status, obj) {
      pbtxt_loading.hide();
      pbtxt.text(response);
      hljs.highlightBlock(pbtxt.get(0));
      pbtxt.show();
      OnGraphChange();
    },
    error: function(obj, err, exc) {
      pbtxt_loading.hide();
      graph_loading.hide();
      pbtxt_error_msg.text(obj['responseText']);
      pbtxt_error.show();
    },
  });
}

var OnGraphChange = function() {
  var pbtxt = $('#pbtxt').text();
  var graph = $('#graph');
  var graph_loading = $('#graph-loading');
  var graph_error = $('#graph-error');

  graph.hide();
  graph_error.hide();

  $.ajax({
    "type": "POST",
    "url": "/api/v1/graph2dot",
    data: pbtxt,
    contentType: "text/plain",
    success: function(response, status, obj) {
      dot = response;
      d3.select("#graph").graphviz().renderDot(dot);
      graph_loading.hide();
      graph.show();
    },
    error: function(obj, err, ex) {
      dot = ''
      pbtxt_loading.hide();
      graph_error.text(obj['responseText']);
      graph_error.show();
    }
  });
}

var CopyToClipboard = function(string) {
  const el = document.createElement('textarea');
  el.value = string;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
};


var OnLoad = function() {
  // Throttle 
  $('#ir-editor').on('change keyup paste', _.throttle(OnIrChange, 1000));

  $('#ir-type').change(function() {
    OnLangChange(true);
    OnIrChange();
  });
  $('#programl-version').change(OnIrChange);

  $('#ir-download').click(function() {
    DownloadText('program' + lang2suffix[currentIrState['type']], editor.getValue());
  });
  $('#pbtxt-download').click(function() {
    DownloadText('program.ProgramGraph.pbtxt', $('#pbtxt').text());
  });
  $('#graph-download').click(function() {
    DownloadText('program.dot', dot);
  });

  $('#share').click(function() {
    uri = AppStateToUri();

    window.location.hash = uri;

    CopyToClipboard(window.location.href);

    alert("Shareable URL copied to clipboard");
  });

  if (window.location.hash.length > 1) {
    SetAppState(window.location.hash);
  }

  OnIrChange();

  editor.focus();
}

// window.addEventListener("hashchange", HashChanged, false);
window.onload = OnLoad;