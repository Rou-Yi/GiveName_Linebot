# https://line-bot-sdk-python.readthedocs.io/en/stable/linebot.models.html#module-linebot.models.flex_message

from linebot.models import FlexSendMessage

personal_setting_message = FlexSendMessage(
  alt_text='個人化設定展示',
  contents={
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "個人化設定",
              "size": "lg",
              "weight": "bold"
            },
            {
              "type": "text",
              "text": "按下更改按鈕可以重新回答該題目喔!",
              "color": "#aaaaaa",
              "size": "sm",
              "offsetTop": "sm"
            },
            {
              "type": "separator",
              "margin": "xl",
              "color": "#323232"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "性別",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans1",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改1"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "none"
                }
              ],
              "margin": "xs",
              "spacing": "sm",
              "offsetTop": "none"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "單雙名",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans2",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改2"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "1px",
                  "gravity": "center"
                }
              ],
              "margin": "xs"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "姓氏",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans3",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改2"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "1px",
                  "gravity": "center"
                }
              ],
              "margin": "xs"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "缺少五行",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans4",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改4"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "1px",
                  "gravity": "center"
                }
              ],
              "margin": "xs"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "加入的字",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans5",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改5"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "1px",
                  "gravity": "center"
                }
              ],
              "margin": "xs"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "加入的音",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans6",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改6"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "1px",
                  "gravity": "center"
                }
              ],
              "margin": "xs"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "常見字",
                  "color": "#aaaaaa",
                  "size": "md",
                  "flex": 3,
                  "margin": "none",
                  "weight": "regular",
                  "style": "normal",
                  "position": "relative",
                  "gravity": "center"
                },
                {
                  "type": "text",
                  "text": "ans7",
                  "color": "#666666",
                  "size": "md",
                  "flex": 3,
                  "weight": "regular",
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "更改",
                    "text": "更改7"
                  },
                  "flex": 3,
                  "height": "sm",
                  "style": "secondary",
                  "position": "relative",
                  "color": "#f9cb9c",
                  "margin": "1px",
                  "gravity": "center"
                }
              ],
              "margin": "xs"
            }
          ],
          "offsetTop": "lg",
          "paddingBottom": "xs"
        }
      ],
      "paddingTop": "lg"
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "spacing": "sm",
      "contents": [],
      "flex": 0
    }
  }
)

message = FlexSendMessage(
  alt_text='個人化設定',
  contents=BubbleContainer(
    size='giga',
    body=BoxComponent(
      layout='vertical',
      padding_top='lg',
      contents=[
        BoxComponent(
          layout='vertical',
          contents=[
            TextComponent(text='個人化設定', size='lg', weight='bold'),
            TextComponent(text='按下更改按鈕可以重新回答該題目喔!', size='sm', color='#aaaaaa', offset_top='sm'),
            SeparatorComponent(margin='xl', color='#323232'),
          ],
        ),
        BoxComponent(
          layout='vertical',
          offset_top='lg',
          padding_bottom='xs',
          contents=[
            flex_button('性別', user_answer),
            flex_button('單雙名', user_answer),
            flex_button('姓氏', user_answer),
            flex_button('五行', user_answer),
            flex_button('加入的音', user_answer),
            flex_button('加入的字', user_answer),
            flex_button('常見字', user_answer),
          ],
        ),
      ],
    )
  )
)