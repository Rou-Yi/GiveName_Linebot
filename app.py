from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import configparser

from question_messages import *
from json_setting import *
from button_menu.personal_setting_template import personal_setting_message
from button_menu.favorite_template import favorite_setting_message
from button_menu.result_template import result_message
from models import expectation_transformer
import random

""" 
Line bot app 基本設定 
"""
app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))


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


# MessageEvent : 收到使用者輸入文字
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id  # str；使用者序號
    text = event.message.text  # str；接收使用者輸入的文字訊息
    user_input = read_json("dataset/user_input.json")  # dict；讀取使用者資料庫
    user_favorite = read_json("dataset/favorite.json")
    user_result = read_json("dataset/result.json")
    registered_ID = list(user_input.keys())  # list；已登錄之使用者ID清單
    wrong_operation, revise_ans = False, False
    reply_all = []

    if user_id not in registered_ID:
        """
        使用者初次使用機器人先引導至「個人化設定」
        """
        print("★ 一位使用者註冊")
        if text == "個人化設定":
            # 題目紀錄機制 : 初始化 False → 輪到該題目時轉為 True → 收到題目回答時轉為回答 text
            user_input[user_id] = {'性別': True, '單雙名': False, '姓氏': False, '五行': False,
                                   '是否加入音': False, '加入的音': False, '是否加入字': False, '加入的字': False,
                                   '常見字': False, '期許': False, '檢測完成': False, '更改答案': False}
            user_favorite[user_id] = {}
            reply_all.append(TextSendMessage(text='接下來請幫我回答一些題目，方便我進行命名推薦~'))
            reply_all.append(question_1_gender)  # 從第一題開始
            print("★ 開始答題")
        else:
            reply_all.append(TextSendMessage(text='初次使用請先點擊下方選單的「個人化設定」進行基本資料填答，才能夠進行寶寶命名喔'))

    elif text == "開始命名":
        """
        當使用者點擊【開始命名】時，在 user_input.json 偵測此為使用者是否已有資料
        若有缺少 → 進入wrong_operation，讓他把題目回答完畢
        若資料完整 → 進入命名系統
        """
        if False not in [x for (_, x) in user_input[user_id].items()][:9]:  # 當前面七題都回答完畢了
            print("★ 使用者進入命名系統，輸入期許")
            reply_all.append(TextSendMessage(text='好的'))
            reply_all.append(TextSendMessage(text='因為小精靈最強大的功能是可以把期望文字轉化為名字'))
            reply_all.append(TextSendMessage(text='所以接下來幫我輸入一下對寶寶的期望或是希望的特質吧!'))
            user_input[user_id]['期許'] = True
            user_input[user_id]['檢測完成'] = False
        else:
            wrong_operation = True

    elif text == "個人化設定":
        """
        當使用者點擊【個人化設定】時，在 user_input.json 偵測此為使用者是否已有資料
        若有缺少 → 進入wrong_operation，讓他把題目回答完畢
        若資料完整 → 展示所有題目的答案
        """
        user_input[user_id]['期許'] = False
        user_input[user_id]['檢測完成'] = False
        if False not in [x for (_, x) in user_input[user_id].items()][:9]:
            reply_all.append(personal_setting_message(user_id))
        else:
            wrong_operation = True

    elif text == "查看我的收藏":
        """
        當使用者點擊【我的收藏】時，顯示此使用者在 user_favorite.json 的資料 
        """
        reply_all.append(favorite_setting_message(user_id))
    # ####################################################################

    elif text[:2] == '刪除':
        print("★ 從收藏中執行刪除名字")
        name = text[2:]
        favorite = user_favorite[user_id]
        if name in favorite:
            del favorite[name]
        save_json(user_favorite, "dataset/favorite.json")
        reply_all.append(favorite_setting_message(user_id))
    # ####################################################################

    elif text[:2] == "收藏":
        """
        使用者從推薦字結果回答後，點選加入我的收藏使用
        """
        favorite_name = text[2:]
        if favorite_name in user_result[user_id]:
            if favorite_name not in user_favorite[user_id]:
                user_favorite[user_id][favorite_name] = user_result[user_id][favorite_name]
                save_json(user_favorite, "dataset/favorite.json")
                reply_all.append(TextSendMessage(text="收藏成功!"))
            else:
                reply_all.append(TextSendMessage(text="「{}」已經在收藏裡面了!".format(favorite_name)))
        else:
            reply_all.append(TextSendMessage(text="我只能幫你收藏最新計算好的名字~"))
    # ####################################################################

    elif text[:2] == "更改":
        """
        使用者從個人化設定中更改回答
        注意：當單雙名選擇單名時，無法添加想要加入的字
        """
        print("★ 從設定中執行更改回答")
        current_question = text[2:]
        if (user_input[user_id]["單雙名"] == "單名") & (current_question == "加入的字"):
            reply_all.append(TextSendMessage(text="不好意思，選擇推薦單名時，無法添增指定加入的字喔"))
            reply_all.append(personal_setting_message(user_id))
        elif (user_input[user_id]["加入的字"] != "") & (current_question == "單雙名"):
            reply_all.append(TextSendMessage(text="不好意思，有指定加入的字時，無法更改為單名喔"))
            reply_all.append(personal_setting_message(user_id))
        else:
            user_input[user_id][current_question] = True
            user_input[user_id]['更改答案'] = True
            if current_question in ["加入的音", "加入的字"]:
                reply_all.append(question_collect[current_question])
                reply_all.append(TextSendMessage(text="(不需要的話，請輸入0)"))
            else:
                reply_all.append(question_collect[current_question])
    # ####################################################################

    elif True in [x for (_, x) in user_input[user_id].items()][:9]:
        """
        啟動命名題目後，一到七題會有題目的狀態是 True
        """
        # current_question: 目前開啟的題目
        current_question = [q_num for (q_num, TF) in user_input[user_id].items() if TF is True][0]

        # 第 一、二、四 題
        if current_question in ["性別", "單雙名", "五行"]:
            if text in question_ans[current_question]:
                # 記錄目前的題目的回答
                index_1 = question_ans[current_question].index(text)
                user_input[user_id][current_question] = save_answer[current_question][index_1]
                # 準備下一題
                index_2 = list(user_input[user_id].keys()).index(current_question)+1
                next_question = list(user_input[user_id].keys())[index_2]
                if not user_input[user_id]['更改答案']:
                    reply_all.append(question_collect[next_question])
                    user_input[user_id][next_question] = True
                else:
                    user_input[user_id]['更改答案'] = False
                    revise_ans = True
            else:
                wrong_operation = True

        # 第 三 題 (會遇到修改)
        elif current_question == "姓氏":
            if text in list(read_json("dataset/xing_dict_1782_new.json").keys()): # 確定在姓氏裡面
                # 記錄目前的題目的回答
                user_input[user_id][current_question] = text
                # 準備下一題
                index_2 = list(user_input[user_id].keys()).index(current_question)+1
                next_question = list(user_input[user_id].keys())[index_2]
                if not user_input[user_id]['更改答案']:
                    reply_all.append(question_collect[next_question])
                    user_input[user_id][next_question] = True
                else:
                    user_input[user_id]['更改答案'] = False
                    revise_ans = True
            else:
                reply_all.append(TextSendMessage(text="請輸入正確的姓氏~"))

        # 第 五、六 題 (是否的題目不會遇到"修改")
        elif current_question in ["是否加入音", "是否加入字"]:
            if text in question_ans[current_question]:
                index_1 = question_ans[current_question].index(text)
                user_input[user_id][current_question] = save_answer[current_question][index_1]
                if index_1:  # index_1 → 是 = 0, 否 = 1
                    index_2 = list(user_input[user_id].keys()).index(current_question)
                    next_question = list(user_input[user_id].keys())[index_2 + 1]  # 加入的音 / 加入的字
                    user_input[user_id][next_question] = ""
                    if (current_question == "是否加入音") & (user_input[user_id]["單雙名"] == "單名"):
                        # 滿足以上條件時，因為單名無法加入字，所以直接跳過加入字的部分
                        # 下一題直接跳往第七題
                        reply_all.append(question_collect["常見字"])
                        user_input[user_id]["常見字"] = True
                        # 第六題答案填充
                        user_input[user_id]["是否加入字"] = "否"
                        user_input[user_id]["加入的字"] = "單名無法加入字"
                    else:
                        next_next_question = list(user_input[user_id].keys())[index_2 + 2]  # 下一題
                        reply_all.append(question_collect[next_next_question])
                        user_input[user_id][next_next_question] = True
                else:
                    index_2 = list(user_input[user_id].keys()).index(current_question) + 1
                    next_question = list(user_input[user_id].keys())[index_2]  # 加入的音 / 加入的字
                    reply_all.append(question_collect[next_question])
                    user_input[user_id][next_question] = True
            else:
                wrong_operation = True

        # 第 五、六 延伸題 (會遇到修改)
        elif current_question in ["加入的音", "加入的字"]:
            if len(text) == 1:
                if (text == "0") or (text == "０"):
                    user_input[user_id][current_question] = ""
                else:
                    # 記錄目前的題目的回答
                    user_input[user_id][current_question] = text
                # 準備下一題
                index_2 = list(user_input[user_id].keys()).index(current_question)+1
                next_question = list(user_input[user_id].keys())[index_2]
                if not user_input[user_id]['更改答案']:
                    reply_all.append(question_collect[next_question])
                    user_input[user_id][next_question] = True
                else:
                    user_input[user_id]['更改答案'] = False
                    revise_ans = True
            else:
                reply_all.append(TextSendMessage(text='僅能輸入一個字哦'))

        elif current_question == '常見字':
            if text in question_ans[current_question]:
                # 記錄目前的題目的回答
                index_1 = question_ans[current_question].index(text)
                user_input[user_id][current_question] = save_answer[current_question][index_1]
                if not user_input[user_id]['更改答案']:
                    # 題目結束回覆
                    reply_all.append(TextSendMessage(text="好了! 謝謝你完成了基本題目回答"))
                    reply_all.append(TextSendMessage(text='如果剛剛有輸入錯誤的題目，可以再按一次「個人化設定」進行更改~'))
                    reply_all.append(TextSendMessage(text='如果都沒有問題的話，請幫我點擊選單中的「開始命名」，進入最後一個步驟吧!'))
                else:
                    user_input[user_id]['更改答案'] = False
                    revise_ans = True
            else:
                wrong_operation = True

    # 紀錄期許回答 + 執行名字推薦系統
    elif user_input[user_id]["期許"] == True:
        print("★ 使用者已完成期許輸入，進入命名推薦系統")
        user_input[user_id]["期許"] = text
        user_input[user_id]['檢測完成'] = True
        line_bot_api.push_message(user_id, [
            TextSendMessage(text='我收到你輸入的期望了!'),
            TextSendMessage(text='請稍等我一下，夢咕嚕現在就開始計算幾個名字給你，計算期間請先不要傳訊息~'),
        ])

    # ####################################################################
    else:
        """ 
        提醒文字，使用者未點擊任何按鈕，但收到使用者輸入時使用 
        """
        error_reply = ['小精靈沒有安裝聊天系統...( ˘•ω•˘ )', '夢咕嚕沒辦法理解你的話...', '哈囉~', '嗨嗨~']
        reply_all.append(TextSendMessage(text=random.choice(error_reply)))
        reply_all.append(TextSendMessage(text='幫我從下方選單中選擇「個人化設定」查看基本資料填答'))
        reply_all.append(TextSendMessage(text='或是選擇「開始命名」讓夢咕嚕為你推薦幾個名字吧'))

    # 存檔
    save_json(user_input, "dataset/user_input.json")
    save_json(user_favorite, "dataset/favorite.json")

    # ####################################################################
    # ####################################################################
    if wrong_operation:
        """
        使用者已進入答題系統，但傳送無法辨識的訊息時使用。給予提醒文字 + 重新傳一次題目
        """
        current_question = [q_num for (q_num, TF) in user_input[user_id].items() if TF is True][0]
        reply_all.append(TextSendMessage(text='請先幫我完成題目回答喔! :D'))
        reply_all.append(question_collect[current_question])

    if user_input[user_id]['檢測完成']:
        """
        使用者完成期許輸入，進入推薦字系統，為了經過存檔而拉出來寫
        """
        transformer = expectation_transformer(user_input[user_id]['期許'])  # 傳喚物件
        print("★ 執行抓取關鍵字模型")
        demand_words = transformer.do_word_filter()  # 執行抓取關鍵字模型
        if demand_words:
            print("★ 開始將關鍵詞轉化為名字推薦字")
            name_recommendation = transformer.get_name(user_input[user_id])  # 將關鍵詞轉化為名字推薦字
            user_input[user_id]['檢測完成'] = False  # 算完就關閉
            if name_recommendation:
                if type(name_recommendation) is str:
                    print("★ 執行中遇到無法計算之情況，跳出計算並給予回覆")
                    reply_all.append(TextSendMessage(text=name_recommendation))
                    reply_all.append(TextSendMessage(text="現在麻煩你到「個人化設定」中進行條件更改"))
                    reply_all.append(TextSendMessage(text="我未來會更努力進行資料庫更新!"))
                else:
                    print("★ 推薦計算執行完畢，給予結束面板")
                    print(name_recommendation)
                    user_result[user_id] = name_recommendation
                    save_json(user_result, "dataset/result.json")  # 存檔
                    line_bot_api.push_message(user_id, [
                        TextSendMessage(text='夢咕嚕把名字計算好了，看看結果吧! (❛◡❛✿)'),
                        result_message(name_recommendation),
                    ])
            else:
                print("★ 使用者輸入的期許抓不到符合所有條件的名字")
                user_input[user_id]['檢測完成'] = False
                reply_all.append(TextSendMessage(text="夢咕嚕抓不到符合所有條件的名字 QQ"))
                reply_all.append(TextSendMessage(text="可以請你幫我多加一點期許嗎? (再按一次「開始命名」)"))
        else:
            print("★ 使用者輸入的期許抓不到關鍵詞")
            user_input[user_id]['檢測完成'] = False
            reply_all.append(TextSendMessage(text="現在輸入的期許好像很難推薦名字耶 QQ"))
            reply_all.append(TextSendMessage(text="可以請你幫我多加一點期許嗎? (再按一次「開始命名」)"))

    # 存檔
    save_json(user_input, "dataset/user_input.json")
    save_json(user_favorite, "dataset/favorite.json")

    if revise_ans:
        """
        使用者透過個人化設定面板修改 1 ~ 7 題的答案，給予提醒文字
        """
        reply_all.append(TextSendMessage(text='修改成功!'))
        reply_all.append(personal_setting_message(user_id))

    if reply_all:
        # 回覆文字訊息
        line_bot_api.reply_message(event.reply_token, reply_all)


if __name__ == "__main__":

    app.run(debug=True)
