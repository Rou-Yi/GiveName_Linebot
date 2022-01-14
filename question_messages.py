from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    MessageTemplateAction,
    QuickReply,
    QuickReplyButton,
    MessageAction,
)

# 第一題 : 性別
question_1_gender = TextSendMessage(
    text="請選擇寶寶的生理性別!",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="女孩", text="她是一位女孩")
            ),
            QuickReplyButton(
                action=MessageAction(label="男孩", text="他是一位男孩")
            ),
            QuickReplyButton(
                action=MessageAction(label="我不想分性別", text="我不想分性別")
            ),
        ]
    )
)

# 第二題 : 單名 or 雙名
question_2_namenum = TextSendMessage(
    text="打算取單名還是雙名呢?",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="單名", text="我要替寶寶取單名")
            ),
            QuickReplyButton(
                action=MessageAction(label="雙名", text="我要替寶寶取雙名")
            ),
        ]
    )
)

# 第三題 : 寶寶的姓氏是什麼呢?
question_3_lastname = TextSendMessage(text='寶寶的姓氏是什麼呢? (文字輸入)')

# 第四題 : 五行
question_4_elements = TextSendMessage(
    text="算命師說過寶寶命中有欠缺什麼五行嗎? 有的話，從下方選擇一項缺少的五行吧",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="沒有缺少", text="沒有缺少")
            ),
            QuickReplyButton(
                action=MessageAction(label="金", text="金")
            ),
            QuickReplyButton(
                action=MessageAction(label="木", text="木")
            ),
            QuickReplyButton(
                action=MessageAction(label="水", text="水")
            ),
            QuickReplyButton(
                action=MessageAction(label="火", text="火")
            ),
            QuickReplyButton(
                action=MessageAction(label="土", text="土")
            ),
        ]
    )
)

# 第五題 : 是否已經有確定要加入的音?
question_5_pronounce = TextSendMessage(
    text="現在有確定要加入的音嗎?",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="有!", text="有! 我想加入特別的音")
            ),
            QuickReplyButton(
                action=MessageAction(label="沒有", text="沒有，我目前沒有一定要加入的音")
            ),
        ]
    )
)

question_5_pronounce_yes = TextSendMessage(text='請輸入任一同音字')


# 第六題 : 是否已經有確定要加入的字?
question_6_character = TextSendMessage(
    text="那麼現在有確定要加入的字嗎?",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="有!", text="有! 我想加入特別的字")
            ),
            QuickReplyButton(
                action=MessageAction(label="沒有", text="沒有，我現在沒有一定要加入的字")
            ),
        ]
    )
)

question_6_character_yes = TextSendMessage(text='要加入什麼字呢？請輸入任一字')

# 第七題 : 是否需要排除常見字?
question_7_commonwords = TextSendMessage(
    text="需要排除常見字嗎?",
    quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label="好啊，我想避開常見的名字", text="好啊，我想避開常見的名字")
            ),
            QuickReplyButton(
                action=MessageAction(label="不用，直接配名字沒關係", text="不用，直接配名字沒關係")
            ),
        ]
    )
)


# 題目統整
question_collect = {'性別': question_1_gender, '單雙名': question_2_namenum, '姓氏': question_3_lastname, '五行': question_4_elements,
                    '是否加入音': question_5_pronounce, '加入的音': question_5_pronounce_yes,
                    '是否加入字': question_6_character, '加入的字': question_6_character_yes,
                    '常見字': question_7_commonwords, '期許': TextSendMessage(text='請輸入一段期許文字喔')}

# 答案統整
question_ans = {"性別": ["她是一位女孩", "他是一位男孩", "我不想分性別"],
                "單雙名": ["我要替寶寶取單名", "我要替寶寶取雙名"],
                "姓氏": [],
                "五行": ["沒有缺少", "金", "木", "水", "火", "土"],
                "是否加入音": ["有! 我想加入特別的音", "沒有，我目前沒有一定要加入的音"],
                "加入的音": [],
                "是否加入字": ["有! 我想加入特別的字", "沒有，我現在沒有一定要加入的字"],
                "加入的字": [],
                "常見字": ["好啊，我想避開常見的名字", "不用，直接配名字沒關係"],
                }

# 儲存指定格式的答案
save_answer = {"性別": ['女孩', '男孩', '其他'], "單雙名": ['單名', '雙名'], "五行": ["無", "金", "木", "水", "火", "土"],
               "是否加入音": ["是", "否"], "是否加入字": ["是", "否"], "常見字": ["過濾掉", "採用"],
               }

