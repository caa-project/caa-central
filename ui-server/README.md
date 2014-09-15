CAA UI Server
=============

# 概要

## Overview

```
  ブラウザ
     ↓ post
Admin Handler  ----  UI Handler ←← 客のブラウザ
     |
     |
Control Proxy
     ↑↓
     ↑↓
Control Server
```


# TODO

- テストについて：control
  serverを起動した状態じゃないとテストできないので，submoduleにしてテストするときに起動したほうがいいかもしれない
