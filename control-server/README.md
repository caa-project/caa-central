CAA Control Server
==================

# API

## arguments
- index ([0-9]+): ロボットのインデックス (idのほうがわかりやすい？)
- passphrase ([a-zA-Z0-9]+): パスフレーズ


## url
- http://host/kill/(index)
indexをクライアントが使えなくする．

- http://host/create/(index)/(passphrase)
index:passphraseの組を登録する．

- ws://host/ws/robo/(index)
ロボットとやりとりをするwebsocketのサーバ．

- http://host/operation/(index)/(passphrase)
ここに命令が書かれたJsonを投げつけるとwebsocketで送信してくれることになっている．
(websocketにした方がいいかも？接続数を１に限定すれば安全．)
