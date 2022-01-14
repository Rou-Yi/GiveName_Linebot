# 快速取得、寫入 json 檔內容的 function

import json

def get_json_file(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as file:
        content = json.load(file)
    return content

def set_json_file(json_filename, content):
    with open(json_filename, 'w', encoding='utf-8') as file:
        jsObj = json.dumps(content)
        file.write(jsObj)
        file.flush()


################### 透過性別選擇資料庫 ###################


'''def get_word_for_gender(gender):
    # 真實世界中的不重複字
    global word_for_gender
    if gender == '男孩':
        word_for_gender = get_json_file('word_for_boy.json')
    elif gender == '女孩':
        word_for_gender = get_json_file('word_for_girl.json')
    elif gender == '其他':
        word_for_gender = get_json_file('word_for_all.json')
    return word_for_gender

def get_vocabulary_list(gender):
    # 真實世界中的不重複字，所有字詞及意義
    global vocabulary_list
    if gender == '男孩':
        vocabulary_list = get_json_file('vocabulary_list_boy.json')
    elif gender == '女孩':
        vocabulary_list = get_json_file('vocabulary_list_girl.json')
    elif gender == '其他':
        vocabulary_list = get_json_file('vocabulary_list_all.json')
    return vocabulary_list

def get_total_words_meaning(gender):
    # 真實姓名中不重複字的所有意義，獨立成額外的一個 list 篩起來比較快
    global total_words_meaning
    if gender == '男孩':
        total_words_meaning = get_json_file('total_words_meaning_boy.json')
    elif gender == '女孩':
        total_words_meaning = get_json_file('total_words_meaning_girl.json')
    elif gender == '其他':
        total_words_meaning = get_json_file('total_words_meaning_all.json')
    return total_words_meaning

def get_meaning_embeddings(gender):
    # 真實姓名中不重複字，對應字詞的 embeddings
    global meaning_embeddings
    if gender == '男孩':
        meaning_embeddings = get_json_file('meaning_embeddings_boy.json')
    elif gender == '女孩':
        meaning_embeddings = get_json_file('meaning_embeddings_girl.json')
    elif gender == '其他':
        meaning_embeddings = get_json_file('meaning_embeddings_all.json')
    return meaning_embeddings

def get_vocabulary_dict(gender):
    # 真實姓名中不重複字，對應的字集和意義
    global vocabulary_dict
    if gender == '男孩':
        vocabulary_dict = get_json_file('vocabulary_dict_boy.json')
    elif gender == '女孩':
        vocabulary_dict = get_json_file('vocabulary_dict_girl.json')
    elif gender == '其他':
        vocabulary_dict = get_json_file('vocabulary_dict_all.json')
    return vocabulary_dict

def get_characteristics_dict(gender):
    # 真實姓名中不重複字，屬性表
    global characteristics_dict
    if gender == '男孩':
        characteristics_dict = get_json_file('characteristics_dict_boy.json')
    elif gender == '女孩':
        characteristics_dict = get_json_file('characteristics_dict_girl.json')
    elif gender == '其他':
        characteristics_dict = get_json_file('characteristics_dict_all.json')
    return characteristics_dict

def get_sounds_dict(gender):
    # 真實姓名中不重複字，同音字庫
    global sounds_dict
    if gender == '男孩':
        sounds_dict = get_json_file('sounds_dict_boy.json')
    elif gender == '女孩':
        sounds_dict = get_json_file('sounds_dict_girl.json')
    elif gender == '其他':
        sounds_dict = get_json_file('sounds_dict_all.json')
    return sounds_dict'''