
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
      $("#info_bar").text("open!");
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
      $("#info_bar").text("close!");
      $("#headerbg").css("background", "#822222");
      ws = null;
    }
  }
  setTimeout(function() { open_websocket(server_url, index, passphrase); }, 1000);
}

function send_data(type, value) {
  var json = JSON.stringify({
    type: type,
    value: value
  });
  append_message('success',json,'');
  if (ws instanceof WebSocket) {
    ws.send(json);
  } else {
    append_message('danger','ws is not instanceof WebSocket','');
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

function is_touch_device() {
    var is_ios = navigator.userAgent.indexOf('iPhone') > 0 ||
        navigator.userAgent.indexOf('iPad') > 0 ||
        navigator.userAgent.indexOf('iPod') > 0;
    var is_android = navigator.userAgent.indexOf('Android') > 0;
    return is_ios || is_android;
}

var timerPool = {
  timers: [],
  push: function(t) {     // 追加
    this.timers.push(t);
  },
  pop: function(t) {      // 削除
    i = this.timers.indexOf(t);
    this.timers.splice(i);
  },
  stopAllTimers: function() {   // すべてのタイマーを止める
    for (var i=0; i<this.timers.length; i++) {
      clearInterval(this.timers[i]);
      this.timers[i] = null;
    }
    this.timers = [];
  }
};

var observer = {
  start: function(action, interval, touch_id) {
    if (this.timer != null)
      return;
    action();
    if (touch_id != null)
      this.touch_id = touch_id
    this.timer = setInterval(action, interval);
    timerPool.push(this.timer);
  },
  finish: function(action, touch_id) {
    if (touch_id != null && touch_id != this.touch_id)
        return;
    if (this.timer != null) {
      if (action != null)
        action();
      clearInterval(this.timer);
      this.tuoch_id = null;
      this.timer = null;
    }
  },
  timer: null,
  touch_id: null
};

/**
 * Set an action to a button. The action is repeated.
 *
 * @param elem {jquery} jQuery object
 * @param action {function} executed repeatedly, started at mousedown
 * @param end_action {function} executed at mouseup event
 * @param interval {int} interval (msec)
 */
function setRepeatedAction(elem, action, end_action, interval) {
  if (is_touch_device()) {
    elem.bind('touchstart', function(e) {
      append_message('info','touchstart','');
      var touches = event.changedTouches;
      observer.start(action, interval,
          touches[0].identifier);
    });
    elem.bind('touchend', function(e) {
      append_message('info','touchend','');
      var touches = event.changedTouches;
      observer.finish(end_action,
          touches[0].identifier);
    });
  } else {
    elem.mousedown(function() {
      console.log("down");
      append_message('info','mousedown','');
      observer.start(action, interval);
    });
    elem.mouseup(function() {
      console.log("up");
      append_message('info','mouseup','');
      observer.finish(end_action);
    });
  }
}

function sendFixedPhrase() {
  send_data("fixedphrase", $("#fixedphrase").val());
}

$(function() {
  var INTERVAL = 5000;   // Less than safety thread interval.

  // 操作ボタン
  // 押している間だけ動くようにする（ボタンを離したらstopする）

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

  $("#btn_fixedphrase").click(sendFixedPhrase);

  if (is_touch_device()) {
    $("#btn_stop").bind('touchstart', function() {
      stop();
      timerPool.stopAllTimers();
    });
    $(window).bind('touchend', function() {
      var touches = event.changedTouches;
      observer.finish(stop, touches[0].identifier);
    });
  } else {
    $("#btn_stop").mousedown(function() {
      stop();
      timerPool.stopAllTimers();
    });
    $(window).mouseup(function() {
      observer.finish(stop);
    });
  }
});
