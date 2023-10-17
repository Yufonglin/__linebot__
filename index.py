from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     print(f"傳傳送的訊息{event.message.text}")
#     #message = TextSendMessage(text=event.message.text)
#     message = TextSendMessage(text="你好")
#     line_bot_api.reply_message(event.reply_token, message)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = ""

    if "你好" in user_message:
        reply_message = "你好！有什么我可以帮助你的吗？"
    elif "天气" in user_message:
        # 在这里添加获取天气信息的代码
        reply_message = "今天天气晴朗！"
    elif "笑话" in user_message:
        # 在这里添加获取笑话的代码
        reply_message = "为什么狗不会上树？因为树上有松鼠！"
    else:
        reply_message = "抱歉，我不太明白你的意思。"

    message = TextSendMessage(text=reply_message)
    line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)