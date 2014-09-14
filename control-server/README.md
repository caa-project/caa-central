CAA Control Server
==================

# 概要
- フレームワークには[tornado](http://www.tornadoweb.org/en/stable/index.html)
- WebSocketのデバッグ用にクライアントは[websocket-client](https://github.com/liris/websocket-client)

UIからAPIを叩いて登録や

# API

## arguments
- index ([0-9]+): ロボットのインデックス (idのほうがわかりやすい？)
- passphrase ([a-zA-Z0-9]+): パスフレーズ


## url
- http://host/delete/(index)
indexをクライアントが使えなくする．

- http://host/register/(index)/(passphrase)
index:passphraseの組を登録する．

- ws://host/robo/(index)
ロボットとやりとりをするwebsocketのサーバ．接続数を１に制限する．

- ws://host/operation/(index)/(passphrase)
UIが命令を送る先．接続数を１に制限する．
