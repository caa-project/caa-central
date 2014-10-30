function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
};

function open_websocket(server_url) {
    var splitted = location.href.split('/')
    var passphrase = splitted.pop()
    var index = splitted.pop()
    var ws = new WebSocket("ws://" + server_url + "/user/" + index + "/" + passphrase);
    //接続開始時の処理
    ws.onopen = function () {
      //ヘッダーに緑地白文字でメッセージを出す
      $("#info_bar").text("connection to " + address + " is opened");
      $("#headerbg").css("background", "#008000");
    }
    //メッセージの受信
    ws.onmessage = function(e) {
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
    //エラーの処理
    ws.onerror = function(error) {
      var log = (new Date()).toLocaleString() + "| " +  error;
      $("#view").html(log + "\n" + $("#view").val());
    };
    //切断時の処理
    ws.onclose = function(e) {
      //ヘッダーに赤地白文字でメッセージを出す
      $("#info_bar").text("connection to " + url + " is closed");
      $("#headerbg").css("background", "#822222");
    }
    function send_view_data() {
      ws.send($("#send_input").val());
    };
    function send_data(val){
      ws.send(val);
    };

    //TODO 他のボタンもclickの動作をここに書く
    // ボタンの動作
    // 押している間だけ動くようにする（ボタンを離したらstopする）
    $("#btn_stop").click(function(){
      send_data("stop");
    });
    // 左
    $("#btn_left").mousedown(function() {
      send_data("left");
    }).mouseup(function() {
      send_data("stop");
    });
    // 右
    $("#btn_right").mousedown(function() {
      send_data("right");
    }).mouseup(function() {
      send_data("stop");
    });
    // 前
    $("#btn_forward").mousedown(function() {
      send_data("forward");
    }).mouseup(function() {
      send_data("stop");
    });
    // 後
    $("#btn_back").mousedown(function() {
      send_data("back");
    }).mouseup(function() {
      send_data("stop");
    });
    // 時計回り
    $("#btn_cw").mousedown(function() {
      send_data("cw");
    }).mouseup(function() {
      send_data("stop");
    });
    // 反時計回り
    $("#btn_ccw").mousedown(function() {
      send_data("ccw");
    }).mouseup(function() {
      send_data("stop");
    });
    // ブレーキ
    $("#btn_brake").mousedown(function() {
      send_data("brake");
    }).mouseup(function() {
      send_data("stop");
    });

    //スライドバーの動作
    $("#anglebar").change(function(){
      var val = $("#anglebar").val();
      var msg = "servo" + val;
      ws.send(msg);
    });
}

