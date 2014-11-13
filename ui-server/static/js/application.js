
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

function wheel(value) {
  return function() {
    send_data("wheel", value);
  };
}

function stop() {
  send_data("wheel", "stop");
}

function say($element) {
  return function() {
    send_data("say", $element.val());
  };
}

function dummy() {}

$(function() {

  //TODO 他のボタンもclickの動作をここに書く
  // ボタンの動作
  // 押している間だけ動くようにする（ボタンを離したらstopする）
  setEvent($("#btn_stop"), stop, dummy, dummy);
  // 左
  setEvent($("#btn_left"), wheel("left"), dummy, stop);
  // 右
  setEvent($("#btn_right"), wheel("right"), dummy, stop);
  // 前
  setEvent($("#btn_forward"), wheel("forward"), dummy, stop);
  // 後
  setEvent($("#btn_back"), wheel("back"), dummy, stop);
  // 時計回り
  setEvent($("#btn_cw"), wheel("cw"), dummy, stop);
  // 反時計回り
  setEvent($("#btn_ccw"), wheel("ccw"), dummy, stop);
  // ブレーキ
  setEvent($("#btn_brake"), wheel("brake"), dummy, stop);

  //スライドバーの動作
  $("#anglebar").change(function() {
    var val = $("#anglebar").val();
    send_data("servo", val);
  });

  setEvent($("#send_btn"), say($("#send_input")), dummy, dummy);

});
