from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (MessageEvent,
                         TextSendMessage, 
                         TemplateSendMessage, 
                         ButtonsTemplate,
                         MessageTemplateAction,
                         PostbackEvent,
                         PostbackTemplateAction)
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    
                    # TextSendMessage(text=event.message.text)
                    #  TextSendMessage(text="ohggg yeah!!!")
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='嗨！我能為你做些什麼嗎？',
                            text='請選擇服務',
                            thumbnail_image_url='https://meet.eslite.com/Content/Images/ArtShow/1047258-penguin_20190116145229.jpg',
                            actions=[
                                PostbackTemplateAction(
                                    label='查看天氣',
                                    text='查看天氣',
                                    data='A&查看天氣'
                                ),
                                 PostbackTemplateAction(
                                    label='東踏曲蜜',
                                    text='東踏曲蜜',
                                    data='B&東踏曲蜜'
                                )
                            ]
                        )
                    )

                )
            elif isinstance(event, PostbackEvent):
                if event.postback.data[0:1] == 'A':
                    line_bot_api.reply_message(
                        event.reply_token,
                         TextSendMessage(text=event.postback.data[0:6])
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()