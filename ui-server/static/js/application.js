
function append_message(tr_class, msg, time) {
  $("#log_tbody").prepend("<tr class=\"" + tr_class + " \"><td>#</td><td>" + msg + "</td><td>" + time + "</td></tr>");
}

var ws = null;

function open_websocket(server_url, index, passphrase) {
  if (ws === null) {
    ws = new WebSocket("ws://" + server_url + "/user/" + index + "/" + passphrase);
    //接続開始時の処理
    ws.onopen = function () {
      //ヘッダーに緑地白文字でメッセージを出す
      $("#info_bar").text("connection to " + server_url + " is opened");
      $("#headerbg").css("background", "#008000");
    }
    //メッセージの受信
    ws.onmessage = function(e) {
      var data = JSON.parse(e.data);
      var time = (new Date()).toLocaleString();
      var tr_class = data["success"] ? "success" : "danger";
      var msg = data["type"] + " : " + data["value"];
      append_message(tr_class, msg, time);
    };
    //エラーの処理
    ws.onerror = function(error) {
      var log = (new Date()).toLocaleString() + "| " +  error;
      $("#view").html(log + "\n" + $("#view").val());
      ws = null;
    };
    //切断時の処理
    ws.onclose = function(e) {
      //ヘッダーに赤地白文字でメッセージを出す
      $("#info_bar").text("connection to " + server_url + " is closed");
      $("#headerbg").css("background", "#822222");
      ws = null;
    }
  }
  setTimeout(function() { open_websocket(server_url, index, passphrase); }, 1000);
}

function send_data(type, value) {
  if (ws instanceof WebSocket)
    ws.send(JSON.stringify({
      type: type,
      value: value
    }));
};

function send_wheel_data(value) {
  send_data("wheel", value);
}

function stop() {
  send_wheel_data("stop");
}

$(function() {

  //TODO 他のボタンもclickの動作をここに書く
  // ボタンの動作
  // 押している間だけ動くようにする（ボタンを離したらstopする）
  $("#btn_stop").click(function(){
    stop();
  });
  // 左
  $("#btn_left").mousedown(function() {
    send_wheel_data("left");
  }).mouseup(function() {
    stop();
  });
  // 右
  $("#btn_right").mousedown(function() {
    send_wheel_data("right");
  }).mouseup(function() {
    stop();
  });
  // 前
  $("#btn_forward").mousedown(function() {
    send_wheel_data("forward");
  }).mouseup(function() {
    stop();
  });
  // 後
  $("#btn_back").mousedown(function() {
    send_wheel_data("back");
  }).mouseup(function() {
    stop();
  });
  // 時計回り
  $("#btn_cw").mousedown(function() {
    send_wheel_data("cw");
  }).mouseup(function() {
    stop();
  });
  // 反時計回り
  $("#btn_ccw").mousedown(function() {
    send_wheel_data("ccw");
  }).mouseup(function() {
    stop();
  });
  // ブレーキ
  $("#btn_brake").mousedown(function() {
    send_wheel_data("brake");
  }).mouseup(function() {
    stop();
  });

  //スライドバーの動作
  $("#anglebar").change(function() {
    var val = $("#anglebar").val();
    send_data("servo", val);
  });

  $("#send_btn").click(function() {
    send_data("say", $("#send_input").val());
  });

});
