# Yunlib BackEnd

[設定教學](https://hackmd.io/@30vhEV7FQECcWeCF1eAN5A/SktUlEHAE)

## Usage

```python
from Yunlib.Yunlib import Yunlib

app = Yunlib('./resource.ini')      # 初始化Yunlib, 載入 resource.ini 設定檔

# 一個簡單的 echo bot 範例
@app.onTextReceivce
def say_it(user_id, reply_token, text):
    app.replyText(reply_token,text)
```

更完整的範例可以參考 app.py 檔案

