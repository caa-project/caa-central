function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

// TODO update address per request
var URL = "ws://echo.websocket.org";

function createWebSocket(url) {

  var ws = new WebSocket(url);

  ws.onopen = function () {
    // Change information on header: green
    $("#info_bar").text("connection to " + url + " is opened");
    $("#headerbg").css("background", "#008000");
  };

  ws.onmessage = function(e) {
    // Loggin messages
    var msg = e.data;
    var time = (new Date()).toLocaleString();
    var tr_class = "";
    if(endsWith(msg, "fail")){
      tr_class = "danger";
    }
    else if(endsWith(msg, "success")){
      tr_class = "success";
    }
    $("#log_tbody").prepend("<tr class=\"" + tr_class + " \"><td>#</td><td>" + msg + "</td><td>" + time + "</td></tr>");
  };

  ws.onerror = function(error) {
    var log = (new Date()).toLocaleString() + "| " +  error;
    $("#view").html(log + "\n" + $("#view").val());
  };

  ws.onclose = function(e) {
    // Change information on header: red
    $("#info_bar").text("connection to " + url + " is closed");
    $("#headerbg").css("background", "#822222");  
  };

  return ws;
}

function prepareButtons(ws) {
  $("#btn_stop").click(function(){
    ws.send("stop");
  });
  // 左
  $("#btn_left").mousedown(function() {
    ws.send("left");
  }).mouseup(function() {
    ws.send("stop");
  });
  // 右
  $("#btn_right").mousedown(function() {
    ws.send("right");
  }).mouseup(function() {
    ws.send("stop");
  });
  // 前
  $("#btn_forward").mousedown(function() {
    ws.send("forward");
  }).mouseup(function() {
    ws.send("stop");
  });
  // 後
  $("#btn_back").mousedown(function() {
    ws.send("back");
  }).mouseup(function() {
    ws.send("stop");
  });
  // 時計回り
  $("#btn_cw").mousedown(function() {
    ws.send("cw");
  }).mouseup(function() {
    ws.send("stop");
  });
  // 反時計回り
  $("#btn_ccw").mousedown(function() {
    ws.send("ccw");
  }).mouseup(function() {
    ws.send("stop");
  });
  // ブレーキ
  $("#btn_brake").mousedown(function() {
    ws.send("brake");
  }).mouseup(function() {
    ws.send("stop");
  });
}

function preparePush(ws) {
  $("#btn_push").click(function() {
    ws.send($("#send_input").val());
  });
}

function prepareSlidebar(ws) {
  $("#anglebar").change(function(){
    var val = $("#anglebar").val();
    var msg = "servo" + val; 
    ws.send(msg);
  });
}


$(function() {
  var ws = createWebSocket(URL);

  prepareButtons(ws);
  preparePush(ws);
  prepareSlidebar(ws);
});
