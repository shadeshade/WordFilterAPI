import os

import requests

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CUR_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')

dict_of_data_sets = dict()
SOURCES_BY_LANG = {
    'en-US': "https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt",
}


def get_data_from_set(lang_code):
    if lang_code not in dict_of_data_sets:
        update_data(lang_code)

    return dict_of_data_sets[lang_code]


def save_data_set(lang_code, words):
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    with open(os.path.join(DATA_DIR, f'words_{lang_code}.txt'), 'w') as f:
        f.write(words)


def update_data(lang_code, ):
    url = SOURCES_BY_LANG.get(lang_code)

    words = None
    try:  # if github doesn't respond, then parse saved file without downloading
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            words = response.text
            save_data_set(lang_code, words)
    except requests.RequestException:
        pass

    if words is None:
        with open(os.path.join(DATA_DIR, f'words_{lang_code}.txt'), 'r') as f:
            words = f.read()

    make_set(lang_code, words)


def initialize_all_data():
    for lang_code in SOURCES_BY_LANG:
        update_data(lang_code)


def make_set(lang_code, words):
    bad_words = set(bw for bw in words.split('\n'))
    dict_of_data_sets[lang_code] = bad_words
