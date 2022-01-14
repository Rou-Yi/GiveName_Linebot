# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# ngrok http 8082


import json

def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        file = json.load(f)
    return file

def save_json(dict, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(dict, f)
        
        
a = read_json("dataset/user_input.json")
a
a['test_ID']
del a['U30c5a55265f4f5eeefe804b0dd52bf85']
del a['Ubd11f5ef426e9aa243c503d477714151']
a['Ubd11f5ef426e9aa243c503d477714151']['五行'] = '無'
save_json(a, "dataset/user_input.json")


a = read_json("dataset/favorite.json")
a
a['test_ID'] = {"美玲":"取自美麗的意思", 
                "怡然":"取自和悅的意思"}
a['U30c5a55265f4f5eeefe804b0dd52bf85'] = {"美玲":"取自美麗的意思", 
                                          "怡然":"取自和悅的意思"}
save_json(a, "dataset/favorite.json")


question = '性別'
a['U30c5a55265f4f5eeefe804b0dd52bf85'][question]
'更改'+question

a = read_json("dataset/wish_category.json")
a
del a['雙名']
save_json(a, "dataset/wish_category.json")


name_recommendation = {'幼惠': {'幼': ['出幼', '長大成人'], '惠': ['特惠', '特別優待']}, '明優': {'明': ['明慧', '聰明'], '優': ['特優', '特別優秀']}}

for name in name_recommendation:
    print(name)
    print(name_recommendation[name])
    name_with_meaning = name_recommendation[name]
    for name_word in name_with_meaning:
        if name_with_meaning[name_word][0] == "個人化設定":
            string = "*源自個人化設定 \n{}".format(name_with_meaning[name_word][1])
        else:
            string = "*取自「{}」 \n意義：{}".format(name_with_meaning[name_word][0], name_with_meaning[name_word][1])
        print(string)


###################################################################################################
###################################################################################################
###################################################################################################

from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
from cnsenti import Sentiment
import re
# Models
# Initialize drivers
ws_driver = CkipWordSegmenter(level=3)  # 斷詞
pos_driver = CkipPosTagger(level=3)  # pos tagging

# Give positive and negative
# https://pypi.org/project/cnsenti/
sentiment_model = Sentiment()

expect_word = ["希望", "期待", "期望", "盼望", "夢想", "祈望", 
               "希冀", "理想", "祈願", "祈禱", "冀望", "有望 "]

class expectation_transformer():
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
        :return: None
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
                # VH (狀態不及物動詞)、VA (動作不及物動詞)、VB(動作類及物動詞)、VI(狀態類及物動詞)
                index = [i for i, x in enumerate(sentence_pos) if x in ["VH", "VA", "VB", "VI"]]
                if index:
                    word_ws = [sentence_ws[i] for i in index]
                    # 判斷為"非負面"語句
                    if sentiment >= 0:
                        self.demand_words.extend(word_ws)
                    # 判斷為"負面"語句，在前面加上【不】作為反義詞
                    elif sentiment < 0:
                        word_ws = ["不" + w for w in word_ws]
                        self.demand_words.extend(word_ws)

                # 職業的關鍵詞【當、當個、成為、變成】，對有關鍵詞的句子過濾出 Na (普通名詞)
                career = [i for i, x in enumerate(sentence_ws) if x in ["當", "當個", "成為", "變成"]]
                if (career != []) & (sentiment >= 0): 
                    for t in career:
                        index = [i for i, x in enumerate(sentence_pos) if (x == "Na") & (i>t)]
                        word_ws = [sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)

                # 對擁有特質的關鍵詞【有(V_2)、富有(VJ)、擁有(VJ)】的斷句過濾出 VJ、V_2，並往後過濾出 Na
                traits = [i for i, x in enumerate(sentence_pos) if x in ["VJ", "V_2"]]
                if (traits != []) & (sentiment >= 0):
                    for t in traits:
                        index = [i for i, x in enumerate(sentence_pos) if (x == "Na") & (i>t)]
                        word_ws = [sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)
                        
                # 過濾狀態XX動詞【狀態句賓動詞(VK)、狀態謂賓動詞(VL)】，並往後過濾出 Na
                another_V = [i for i, x in enumerate(sentence_pos) if (x in ["VK", "VL"]) & (sentence_ws[i] not in expect_word)]
                if (another_V != []) & (sentiment >= 0):
                    for t in another_V:
                        index = [i for i, x in enumerate(sentence_pos) if (x == "Na") & (i>t)]
                        word_ws = [sentence_ws[i] for i in index]
                        self.demand_words.extend(word_ws)
                
        # 最終留下來的字詞
        self.demand_words = list(set(self.demand_words))
        #return self.demand_words


transformer = expectation_transformer("我希望我的孩子做事有條理，擁有好奇心，富有創意感，擅長運動，喜愛畫畫、唱歌跳舞樣樣行")
transformer.do_word_filter()
transformer.pos
transformer.demand_words

