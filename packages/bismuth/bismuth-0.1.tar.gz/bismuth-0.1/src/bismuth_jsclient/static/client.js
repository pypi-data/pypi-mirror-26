'use strict';

(function(module) {

  var ws;
  var displayArea;
  var form;
  var formText;
  var formButton;

  function connect() {
    return new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/ws");
  }

  function readBlob(blob, callback) {
    var reader = new FileReader();
    reader.addEventListener('loadend', function() {
      callback(reader.result);
    });
    reader.readAsBinaryString(blob);
  }

  function displayMessage(text) {
    var el = document.createElement('div');
    el.classList.add('message');
    var label = document.createElement('span');
    label.classList.add('timestamp');
    label.appendChild(document.createTextNode(new Date().toISOString()));
    el.appendChild(label);
    el.appendChild(document.createTextNode(text));
    displayArea.appendChild(el);
    form.scrollIntoView();
  }

  function receive(message) {
    var content = message.data;
    if (content.constructor === Blob) {
      readBlob(content, function(text) { displayMessage("binary: " + JSON.stringify(text)); });
    } else {
      displayMessage("text: " + content);
    }
  }

  function closed(event) {
    displayMessage(
      "closed: code " + event.code +
      ", reason: " + JSON.stringify(event.reason) +
      ", clean: " + event.wasClean
    );
    ws = null;
  }

  function initiate() {
    ws = connect();
    ws.onmessage = receive;
    ws.onclose = closed;
    displayArea = document.getElementById('display');
    form = document.getElementById('input');
    formText = document.getElementById('message-text');
    formButton = document.getElementById('message-send');
    form.onsubmit = formButton.onclick = sendFromForm;
  }

  function close() {
    if (ws != null) {
      ws.close();
      ws = form = formText = formButton = null;
    }
  }

  function send(data) {
    ws.send(data);
  }

  function sendFromForm(event) {
    if (ws != null) {
      send(formText.value);
      formText.value = "";
    }
    event.preventDefault();
  }

  module.bismuth = {
    connect: initiate,
    close: close,
    send: send,
  };

})(window);
