# Yunlib BackEnd

[設定教學](https://hackmd.io/s/BkWQymXoV)

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

## doc

### Yunlib

| method | function |
| --------------- | -------- |
| .onTextReceive() | decorator, 收到文字訊息時觸發對應 method |
| .onPostbackReceive() | decorator, 收到Postback時觸發 method |
| .onUserFollow() | decorator, 被follow時觸發 |
| .onUserUnfollow() | decorator, 被解除追蹤觸發 |
| .pushText(user_id, msg) | 主動推送訊息至user |
| .pushBookList(user_id, booklist, alt_text='[Book list]' | 主動推送Booklist |
| .replyText(reply_token, message) | 對user回文字訊息 |
| .replyBookList(reply_token, booklist, alt_text='[Book list]') | 對user回 Booklist |
| .changeRichMenu(user_id, menu_name) | 更改使用者的 rich menu |
| .updateNotificationSetting(user_id, boolval) | 關閉或開啟使用者的到期通知 |

### Yunlib.database

| method | function |
| --------------- | -------- |
| .database.userinfo.querys() | 從userinfo table取得所有的資料 |
| .database.userinfo.insert(user_id, notify = True, note = None) | 對 userinfo table 新增一筆資料 |
| .database.userinfo.query_by_id(user_id) | 從userinfo table中取得對應user_id的資料 |
| .database.userinfo.update_notify(user_id, value) | 更新某 user 的 notify 到期通知開關 |
| .database.userinfo.is_notify_on(user_id) | 回傳一個布林值,表示某user的到期通知是否開啟 |
| .database.userinfo.delete(user_id) | 刪除某user的資料 |

### Yunlib.cloader

| property | function |
| -------- | -------- |
| .cloader.library_id | 取得使用者的圖書館 id |
| .cloader.library_pwd | 取得使用者的圖書館密碼 | 
