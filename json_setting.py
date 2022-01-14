import json, csv


def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        file = json.load(f)
    return file


def save_json(dict, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(dict, f)


def get_json_file(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as file:
        content = json.load(file)
    return content


def set_json_file(json_filename, content):
    with open(json_filename, 'w', encoding='utf-8') as file:
        jsObj = json.dumps(content)
        file.write(jsObj)
        file.flush()


def get_csv_file(csv_filename):
    content = []
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            content.append(row)
    return content

