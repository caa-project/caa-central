CAA Control Server
==================

# API

## arguments
- index ([0-9]+): ロボットのインデックス (idのほうがわかりやすい？)
- passphrase ([a-zA-Z0-9]+): パスフレーズ


## url
- http://host/delete/(index)
indexをクライアントが使えなくする．

- http://host/register/(index)/(passphrase)
index:passphraseの組を登録する．

- ws://host/ws/robo/(index)
ロボットとやりとりをするwebsocketのサーバ．接続数を１に制限する．

- ws://host/operation/(index)/(passphrase)
UIが命令を送る先．接続数を１に制限する．
