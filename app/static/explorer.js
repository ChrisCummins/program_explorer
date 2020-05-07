hljs.initHighlightingOnLoad();

var editor = ace.edit("ir-editor", {
  autoScrollEditorIntoView: true,
  maxLines: 50,
  minLines: 30
});

// Cache the current state of IR to compare against in event callbacks.
var currentIrState = {
  "ir": null,
  "type": null,
  "version": null,
};

// A map from IR type names to file suffixes, used to generate the file extension
// for the "Download" button.
var type2suffix = {
  "LLVM 6.0.0": ".ll",
  "XLA HLO": ".pbtxt",
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
    t: currentIrState['type'],
    v: currentIrState['version'],
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
  $('#programl-version').val(state.v);
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

var OnIrChange = function() {
  // DOM elements.
  var pbtxt_loading = $('#pbtxt-loading');
  var graph = $('#graph');
  var graph_loading = $('#graph-loading');

  var ir_type = $('#ir-type').children("option:selected").val();
  var version = $('#programl-version').children("option:selected").val();
  var pbtxt = $('#pbtxt');
  var pbtxt_error = $('#pbtxt-error');
  var pbtxt_error_msg = $('#pbtxt-error .message');
  var graph_error = $('#graph-error');

  var ir = editor.getValue();

  // Chekc if the state of the IR has changed, so that we know it needs
  // re-rendering.
  var newIrState = {
    "ir": ir,
    "type": ir_type,
    "version": version,
  }
  if (currentIrState['type'] === newIrState['type'] &&
    currentIrState['version'] === newIrState['version'] &&
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
    url: "/api/v1/ir2graph",
    data: JSON.stringify(newIrState),
    contentType: "application/json",
    success: function(response, status, obj) {
      pbtxt_loading.hide();
      pbtxt.text(response['graph']);
      hljs.highlightBlock(pbtxt.get(0));
      pbtxt.show();
      OnGraphChange();
    },
    error: function(obj, err, exc) {
      pbtxt_loading.hide();
      graph_loading.hide();

      response = JSON.parse(obj['responseText']);
      if (response['error']) {
        pbtxt_error_msg.text(response['error']);
      } else {
        pbtxt_error_msg.text(response["message"]);
      }
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

  request = {
    "graph": pbtxt,
  }

  $.ajax({
    "type": "POST",
    "url": "/api/v1/graph2dot",
    data: JSON.stringify(request),
    contentType: "application/json",
    success: function(response, status, obj) {
      dot = response['dot'];
      d3.select("#graph").graphviz().renderDot(dot);
      graph_loading.hide();
      graph.show();
    },
    error: function(obj, err, ex) {
      dot = ''
      pbtxt_loading.hide();
      response = JSON.parse(obj['responseText']);
      if (response['error']) {
        graph_error.text(response['error']);
      } else {
        graph_error.text(response["message"])
      }
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

  $('#ir-type').change(OnIrChange);

  $('#ir-download').click(function() {
    DownloadText('program' + type2suffix[currentIrState['type']], editor.getValue());
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