
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
  json = JSON.stringify({
    type: type,
    value: value
  });
  if (ws instanceof WebSocket) {
    ws.send(json);
  }
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


/**
 * Set an action to a button. The action is repeated.
 *
 * @param elem {jquery} jQuery object
 * @param action {function} executed repeatedly, started at mousedown
 * @param end_action {function} executed at mouseup event
 * @param interval {int} interval (msec)
 */
function setRepeatedAction(elem, action, end_action, interval) {
  var timer = {
    start: function() {
      this.timer = null;
      action();
      if (this.timer == null) {
        this.timer = setInterval(action, interval); 
      }
    },
    finish: function() {
      end_action();
      if (this.timer != null) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
  };
  if (window.TouchEvent) {
    elem.get(0).addEventListener("touchstart", function(e) {
      timer.start();
    });
    elem.get(0).addEventListener("touchend", function(e) {
      timer.finish();
    });
  }
  elem.mousedown(function() {
    console.log("down");
    timer.start();
  });
  elem.mouseup(function() {
    console.log("up");
    timer.finish();
  });
}


$(function() {
  var INTERVAL = 5000;   // Less than safety thread interval.

  // 操作ボタン
  // 押している間だけ動くようにする（ボタンを離したらstopする）
  
  $('#btn_stop').click(stop);

  // 左
  setRepeatedAction($("#btn_left"), wheel("left"), stop, INTERVAL);
  // 右
  setRepeatedAction($("#btn_right"), wheel("right"), stop, INTERVAL);
  // 前
  setRepeatedAction($("#btn_forward"), wheel("forward"), stop, INTERVAL);
  // 後
  setRepeatedAction($("#btn_back"), wheel("back"), stop, INTERVAL);
  // 時計回り
  setRepeatedAction($("#btn_cw"), wheel("cw"), stop, INTERVAL);
  // 反時計回り
  setRepeatedAction($("#btn_ccw"), wheel("ccw"), stop, INTERVAL);
  // ブレーキ
  setRepeatedAction($("#btn_brake"), wheel("brake"), stop, INTERVAL);

  // スライドバーの動作
  // $("#anglebar").change(function() {
  //   var val = $("#anglebar").val();
  //   send_data("servo", val);
  // });

  // 送信ボタン
  $("#send_btn").click(say($("#send_input")));
});
