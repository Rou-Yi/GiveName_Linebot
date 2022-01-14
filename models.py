from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
from cnsenti import Sentiment
import re
from json_setting import *
import time
from collections import OrderedDict
from sentence_transformers import SentenceTransformer, util

# Python Files
from api import *
from good_bad import *
from xing_name_ele import *

"""
分解期望文字的模型
"""
# Models
# Initialize drivers
ws_driver = CkipWordSegmenter(level=3)  # 斷詞
pos_driver = CkipPosTagger(level=3)  # pos tagging

# Give positive and negative
# https://pypi.org/project/cnsenti/
sentiment_model = Sentiment()

"""
將期望關鍵詞轉化為名字的模型
"""
# Models --- for select name words
model = SentenceTransformer('D:/Class/AI_bot/distiluse-base-multilingual-cased-v2')
print("Load Models")

expect_word = ["希望", "期待", "期望", "盼望", "夢想", "祈望",
               "希冀", "理想", "祈願", "祈禱", "冀望", "有望 "]


class expectation_transformer:
    """
    從使用者輸入的期望語句中，擷取需要的詞彙 demand_words，最後產生名字推薦清單
    """
    def __init__(self, expectation_text):
        punctuation = '，,。、.！!？?；;%$#「」『』【】'  # 以所有標點符號為斷句
        self.text = re.sub("[{}]+".format(punctuation), " ", expectation_text).split(" ")
        self.pos_neg_list = []
        self.demand_words = []

        # Run pipeline
        self.ws = ws_driver(self.text)
        self.pos = pos_driver(self.ws)

    def do_word_filter(self):
        """
        分解期望文字，並擷取需要的關鍵詞
        """
        # sentiment detector
        for i in self.text:
            sentiment = sentiment_model.sentiment_calculate(i)
            if sentiment['pos'] > sentiment['neg']:
                self.pos_neg_list.append(1)  # 正面
            elif sentiment['pos'] < sentiment['neg']:
                self.pos_neg_list.append(-1)  # 負面
            else:
                self.pos_neg_list.append(0)  # 中立

        # 從期望中擷取需要的詞彙
        # https://ckip.iis.sinica.edu.tw/service/transformers/ 最上方有【標記列表】
        for sentence, sentence_ws, sentence_pos, sentiment in zip(self.text, self.ws, self.pos, self.pos_neg_list):
            # print(sentence_ws)
            # print(sentence_pos)
            if sentence_ws:
                # 對每一個斷句過濾出指定 pos
                # VH(狀態不及物動詞)、VA(動作不及物動詞)、VB(動作類及物動詞)、VI(狀態類及物動詞)
                index = [i for i, x in enumerate(sentence_pos) if x in ["VH", "VA", "VB", "VI"]]
                if index:
                    word_ws = [sentence_ws[i] for i in index]
                    # 判斷為"非負面"語句
                    if sentiment >= 0:
                        self.demand_words.extend(word_ws)
                    # 判斷為"負面"語句，在前面加上【不】作為反義詞  → 不採用
                    """
                    elif sentiment < 0:
                        word_ws = ["不" + w for w in word_ws]
                        self.demand_words.extend(word_ws)
                    """

                # 職業的關鍵詞【當、當個、成為、變成】，對有關鍵詞的句子過濾出 Na (普通名詞)  → 不採用
                """
                career = ["老師", "教師", "教授", "醫生", "醫師", "牙醫", "護士", "護理師", "工程師",
                          "律師", "科學家", "企業家", "公務人員", "公務員", "老闆"]
                index = [i for i, x in enumerate(sentence_ws) if x in career]
                if career:
                    if sentiment >= 0:
                        word_ws = [sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)
                    else:
                        word_ws = ["不要成為"+sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)
                """
                # 對擁有特質的關鍵詞【有(V_2)、富有(VJ)、擁有(VJ)】的斷句過濾出 VJ、V_2，並往後過濾出 Na
                traits = [i for i, x in enumerate(sentence_pos) if x in ["VJ", "V_2"]]
                if (traits != []) & (sentiment >= 0):
                    for t in traits:
                        index = [i for i, x in enumerate(sentence_pos) if (x == "Na") & (i > t)]
                        word_ws = [sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)

                # 過濾狀態XX動詞【狀態句賓動詞(VK)、狀態謂賓動詞(VL)】，並往後過濾出 Na
                another_V = [i for i, x in enumerate(sentence_pos) if
                             (x in ["VK", "VL"]) & (sentence_ws[i] not in expect_word)]
                if (another_V != []) & (sentiment >= 0):
                    for t in another_V:
                        index = [i for i, x in enumerate(sentence_pos) if (x == "Na") & (i > t)]
                        word_ws = [sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)

        # 最終留下來的字詞
        self.demand_words = list(set(self.demand_words))
        return self.demand_words

    def get_name(self, user_answer):
        gender = user_answer['性別']
        mode = user_answer['單雙名']
        xing = user_answer['姓氏']
        add_ele = user_answer['五行']
        sound = user_answer['加入的音']
        popular = user_answer['常見字']
        demand = self.demand_words

        if user_answer['加入的字'] == '單名無法加入字':
            decided = ""
        else:
            decided = user_answer['加入的字']

        # basic settings
        standard = 0.8  # 相似度下限
        item_num = round(30/len(demand))  # 取相似度最高的前多少項

        name_start = time.time()

        # 透過性別取得資料庫
        if gender == '男孩':
            word_for_gender = get_json_file('dataset/word_for_boy.json')
            vocabulary_list = get_json_file('dataset/vocabulary_list_boy.json')
            total_words_meaning = get_json_file('dataset/total_words_meaning_boy.json')
            meaning_embeddings = get_json_file('dataset/meaning_embeddings_boy.json')
            vocabulary_dict = get_json_file('dataset/vocabulary_dict_boy.json')
            characteristics_dict = get_json_file('dataset/characteristics_dict_boy.json')
            sounds_dict = get_json_file('dataset/sounds_dict_boy.json')
        elif gender == '女孩':
            word_for_gender = get_json_file('dataset/word_for_girl.json')
            vocabulary_list = get_json_file('dataset/vocabulary_list_girl.json')
            total_words_meaning = get_json_file('dataset/total_words_meaning_girl.json')
            meaning_embeddings = get_json_file('dataset/meaning_embeddings_girl.json')
            vocabulary_dict = get_json_file('dataset/vocabulary_dict_girl.json')
            characteristics_dict = get_json_file('dataset/characteristics_dict_girl.json')
            sounds_dict = get_json_file('dataset/sounds_dict_girl.json')
        else:
            word_for_gender = get_json_file('dataset/word_for_all.json')
            vocabulary_list = get_json_file('dataset/vocabulary_list_all.json')
            total_words_meaning = get_json_file('dataset/total_words_meaning_all.json')
            meaning_embeddings = get_json_file('dataset/meaning_embeddings_all.json')
            vocabulary_dict = get_json_file('dataset/vocabulary_dict_all.json')
            characteristics_dict = get_json_file('dataset/characteristics_dict_all.json')
            sounds_dict = get_json_file('dataset/sounds_dict_all.json')

        '''word_for_gender = get_word_for_gender(gender)
        vocabulary_list = get_vocabulary_list(gender)
        total_words_meaning = get_total_words_meaning(gender)
        meaning_embeddings = get_meaning_embeddings(gender)
        vocabulary_dict = get_vocabulary_dict(gender)
        characteristics_dict = get_characteristics_dict(gender)
        sounds_dict = get_sounds_dict(gender)'''

        # 教育部字典裡所有字的讀音
        moe_sounds_dict = get_json_file('dataset/moe_sounds_dict.json')
        moe_bihua_dict = get_json_file('dataset/moe_bihua_dict.json')
        # 台灣 1782 個登記在冊，且打字打得出來的姓氏
        xing_dict = get_json_file('dataset/xing_dict_1782_new.json')

        if (decided != '') and (decided not in list(moe_bihua_dict.keys())):
            return '不好意思，夢咕嚕在教育部字典裡找不到你想要加入的字'

        # 姓氏五行屬性
        xing_ele = xing_dict[xing]['五行']
        xing_stroke = sum(xing_dict[xing]['筆畫'])

        if mode == '單名':
            name_ele = xing_name_ele[xing_ele][0]
            if add_ele != '無':
                name_ele = add_ele  # 單名，加上缺五行
            else:
                pass
        elif mode == '雙名':
            name_ele = xing_name_ele[xing_ele]
            if add_ele != '無':
                if add_ele not in name_ele[-1]:
                    name_ele[-1].append(add_ele)
                    name_ele = [[name_ele[0], add_ele], name_ele[-1]]  # 雙名，加上缺五行，但未篩選

        print('姓氏 =', xing, '| 筆畫 =', xing_stroke, '| 五行 =', xing_ele, '| 模式 =', mode)
        print('名字的五行架構 =', name_ele)

        start = time.time()

        total_result = []  # 所有期許的推薦字
        total_meaning = {}  # 所有期許的推薦字、對應字詞、字詞意義

        # 檢查 gender 是否在 wish category 中
        check_gender = get_json_file('dataset/wish_category.json')
        if gender not in list(check_gender.keys()):
            check_gender[gender] = {}
        set_json_file('dataset/wish_category.json', check_gender)

        # 檢查 wish_category.json 中有沒有一樣的期許
        check_category = get_json_file('dataset/wish_category.json')

        for wish in demand:
            if wish not in list(check_category[gender].keys()):
                coefs = []
                demand_embeddings = model.encode(wish)
                for i in range(len(meaning_embeddings)):
                    similarity = util.pytorch_cos_sim(demand_embeddings, meaning_embeddings[i])
                    coef = str(similarity).split('[[')[1].split(']]')[0]
                    coefs.append(eval(coef))
                    # print(round((i + 1) * 100 / len(meaning_embeddings)), '%')  # 把相似度分析的進度 print 出來

                group = {}
                for i in range(len(coefs)):
                    if coefs[i] > standard:
                        group[coefs[i]] = total_words_meaning[i]

                sorted_group = {}
                coefficient_set = sorted(group.keys(), reverse=True)

                # 把類別記錄進 wish_category.json
                category = {}
                for i in range(len(coefficient_set)):
                    category[coefficient_set[i]] = group.get(coefficient_set[i])

                wish_category = get_json_file('dataset/wish_category.json')

                if wish not in list(wish_category[gender].keys()):
                    wish_category[gender][wish] = category
                    set_json_file('dataset/wish_category.json', wish_category)
                else:
                    pass

                # 取前 30/n 項
                if len(coefficient_set) > item_num:
                    for i in range(item_num):
                        sorted_group[coefficient_set[i]] = group.get(coefficient_set[i])
                else:
                    for i in range(len(coefficient_set)):
                        sorted_group[coefficient_set[i]] = group.get(coefficient_set[i])

            # 如果 wish 已經被記錄過
            else:
                sorted_group = {}
                coefficient_set = list(check_category[gender][wish].keys())
                if len(coefficient_set) > item_num:
                    coefficient_set = coefficient_set[:item_num]
                for i in coefficient_set:
                    sorted_group[i] = check_category[gender][wish][i]

            print('\n關鍵字 =', wish, '| 相似度下限 = 至少 >', standard, '| 取相似度最高的前', item_num, '項')
            #print('\n相似詞義 =', sorted_group)

            result = []
            meaning_dict = {}

            for i in sorted_group:
                meaning = sorted_group.get(i)
                for word in vocabulary_dict:
                    for vocabulary in vocabulary_dict[word]:
                        target = vocabulary[1]
                        if target == meaning:
                            result.append(word)
                            meaning_dict[vocabulary[0]] = meaning
                            if word not in total_result:
                                total_result.append(word)
                                total_meaning[word] = [vocabulary[0], meaning]

            result = list(OrderedDict.fromkeys(result))

            #print('\n推薦字 =', result)
            print('\n對應詞彙及意義 =', meaning_dict)
            print('\n----------------------------------')
        end = time.time()
        #print('\n耗時', format(end - start), '秒')  # 執行所有關鍵字的相似度分析所需要的時間
        print('共推薦', len(total_result), '個字如下:\n', total_result, '\n')

        # 如果有要求的讀音，列出同音字
        sound_words = []
        if sound != '':
            ph = moe_sounds_dict[sound]
            for i in ph:
                if i in list(sounds_dict.keys()):
                    sound_words += sounds_dict[i]
            print('同音字 =', sound_words)

            if sound_words != []:

                suggest_name = []

                if mode == '單名':
                    suggest_name = sound_words
                else:  # 雙名的狀況
                    for i in sound_words:
                        for j in total_result:
                            if i != j:  # 篩掉名字中的兩個字相同的組合
                                # 篩掉頭重腳輕的組合
                                if characteristics_dict[i]['筆畫'] == characteristics_dict[j]['筆畫']:
                                    suggest_name.append(i + j)
                                    suggest_name.append(j + i)
                                elif characteristics_dict[i]['筆畫'] < characteristics_dict[j]['筆畫']:
                                    suggest_name.append(i + j)
                                else:
                                    suggest_name.append(j + i)
                print('依據同音所推薦出來的名字 =', suggest_name)
            else:
                return '不好意思，夢咕嚕在資料庫中找不到你所輸入的字音'

        # 沒有設定同音字的狀況才篩五行
        else:
            # 從期許字中挑出符合姓氏五行屬性的名字推薦字
            ele_o = []
            ele_x = []

            for i in total_result:
                if characteristics_dict[i]['五行'] in name_ele[-1]:
                    ele_o.append(i)
                else:
                    ele_x.append(i)

            print('期許字中符合五行的字 =', ele_o)
            #print('期許字中不符合五行的字 =', ele_x, '\n')

            # 單名 = 期許字中符合五行的字
            # 雙名 # 篩掉名字兩個字相同的組合 # 篩掉頭重腳輕組合
            if mode == '單名':
                suggest_name = ele_o
            elif mode == '雙名':
                suggest_name = []
                for i in ele_o:
                    for j in ele_o:
                        if j != i:  # 篩掉名字兩個字相同的組合
                            if characteristics_dict[i]['筆畫'] <= characteristics_dict[j]['筆畫']:  # 篩掉頭重腳輕組合
                                if characteristics_dict[i]['五行'] in name_ele[0]:  # 名字符合五行架構
                                    suggest_name.append(i + j)
            #print('符合五行架構的名字 =', suggest_name)
            #print(len(suggest_name))

            # 篩掉不符合缺五行 # 單名雙名皆可篩，但基本上單名一定符合
            for i in suggest_name:
                if add_ele not in [characteristics_dict[i[0]]['五行'], characteristics_dict[i[-1]]['五行']]:
                    suggest_name.remove(i)
            #print('符合缺少的五行架構的名字 =', suggest_name)
            #print(len(suggest_name))

        # 單名 #篩掉該字為常用字的狀況
        # 雙名 #篩掉兩個字都是常用字的狀況
        if popular == '過濾掉':
            for i in suggest_name:
                if (characteristics_dict[i[0]]['是否常用'] == '是') and (characteristics_dict[i[-1]]['是否常用'] == '是'):
                    suggest_name.remove(i)
        else:
            pass
        print('符合五行、缺五行、不皆為常用字的名字 =', suggest_name)
        print(len(suggest_name))

        # 加入確定加入的字
        # 只會有雙名的狀況，單名應該在輸入時已排除
        # 在這個狀況下，只能確保另一個字符合五行架構
        if sound == '':
            if (decided != ''):
                original_len = len(suggest_name)
                for i in range(original_len):
                    # 篩掉名字中的兩個字重複
                    if decided != suggest_name[i][-1]:
                        # 篩掉頭重腳輕
                        if moe_bihua_dict[decided] <= characteristics_dict[suggest_name[i][-1]]['筆畫']:
                            suggest_name.append(decided + suggest_name[i][-1])
                    # 篩掉名字中的兩個字重複
                    if decided != suggest_name[i][0]:
                        # 篩掉頭重腳輕
                        if characteristics_dict[suggest_name[i][0]]['筆畫'] <= moe_bihua_dict[decided]:
                            suggest_name.append(suggest_name[i][0] + decided)
                suggest_name = suggest_name[original_len:]
                suggest_name = list(OrderedDict.fromkeys(suggest_name))
                # print('符合確定加入字的名字 =', suggest_name)
                # print(len(suggest_name))
            else:
                pass
                # print('沒有確定加入字 =', suggest_name)
                # print(len(suggest_name))
        else:
            if (decided != ''):
                suggest_name = []
                for i in sound_words:
                    if i != decided:
                        if characteristics_dict[i]['筆畫'] <= moe_bihua_dict[decided]:
                            suggest_name.append(i + decided)
                        if moe_bihua_dict[decided] <= characteristics_dict[i]['筆畫']:
                            suggest_name.append(decided + i)
        print(suggest_name)
        # print(len(suggest_name))

        # 五格計算
        # 單名 # 雙名
        # 天格只考慮姓氏，和名字無關
        name_destiny = {}
        sorted_name_destiny = {}

        for i in suggest_name:
            # 人格
            ren = xing_dict[xing]['筆畫'][-1] + moe_bihua_dict[i[0]]

            # 地格
            if mode == '單名':
                di = moe_bihua_dict[i]
            elif mode == '雙名':
                di = moe_bihua_dict[i[0]] + moe_bihua_dict[i[1]]

            # 總格
            zong = sum(xing_dict[xing]['筆畫']) + di

            # 外格
            if len(xing) == 1:
                if mode == '單名':
                    wai = 2
                elif mode == '雙名':
                    wai = zong - ren + 1
            elif len(xing) == 2:
                wai = zong - ren

            destiny = [ren, di, zong, wai]
            destiny_num = 0
            for d in destiny:
                ji_xong = good_bad[str(d)]
                if ji_xong == '吉':
                    destiny_num += 2
                elif ji_xong == '吉帶凶':
                    destiny_num += 1
                elif ji_xong == '凶帶吉':
                    destiny_num -= 1
                elif ji_xong == '凶':
                    destiny_num -= 2
            name_destiny[i] = destiny_num

        # dictionary sorting by index
        ke = list(name_destiny.keys())
        rank_sort_key = sorted(ke, key=lambda ke: name_destiny[ke], reverse=True)
        for i in rank_sort_key:
            sorted_name_destiny[i] = name_destiny[i]
        # print('姓名吉祥程度排序 =', sorted_name_destiny)

        # print(total_meaning)
        # 每個名字的來源及其意義
        final = {}
        for i in sorted_name_destiny:
            if mode == '單名':
                """
                if i in list(total_meaning.keys()):
                    source_meaning = total_meaning[i]
                    final[i] = source_meaning
                elif i in sound_words:
                    final[i] = ['個人化設定', '同音字']
                """
                if i in list(total_meaning.keys()):
                    source_meaning = total_meaning[i]
                elif i in sound_words:
                    source_meaning = ['個人化設定', '同音字']
                final[i] = {i: source_meaning}

            # 雙名
            else:
                if i[0] in list(total_meaning.keys()):
                    source_meaning1 = total_meaning[i[0]]
                elif i[0] in sound_words:
                    source_meaning1 = ['個人化設定', '同音字']
                else:
                    source_meaning1 = ['個人化設定', '確定加入字']

                if i[1] in list(total_meaning.keys()):
                    source_meaning2 = total_meaning[i[1]]
                elif i[1] in sound_words:
                    source_meaning2 = ['個人化設定', '同音字']
                else:
                    source_meaning2 = ['個人化設定', '確定加入字']

                final[i] = {i[0]: source_meaning1, i[1]: source_meaning2}

        if len(list(final.keys())) > 10:
            for i in list(final.keys())[10:]:
                del final[i]

        #print('final =', final)
        name_end = time.time()
        print('此次命名耗時', round(name_end - name_start), '秒, 共產出', len(list(final.keys())), '個名字(最多10個)\n')

        return final

