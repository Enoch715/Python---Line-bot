from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('49B3Uyg8fH9+K7UDdwNnu6XKEbQCWbYG0Z1+VI9Ozz8X1IQsOjnQfBtbwQ622XidUyvrIV35b0OrhdvVVxlqQY5doyJOXwQvbLBKpsuhOhrS+VvetlVNgL9kHULU23uFS8ddLVamEbPbyX46vmXi9wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('28610dfddc4c40de63105a743d75c7c8')



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂你說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
        package_id='11537',
        sticker_id='52002763'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg in ['hi', 'Hi']:
        r = '哈囉，您好'
    elif msg == '你吃飯了嗎?':
        r = '還沒'
    elif msg == '你是誰?':
        r ='我是機器人'
    elif '訂位' in msg:
        r = '你想訂位是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()