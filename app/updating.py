import os
from flask_restful import abort

import requests

from app.filtering import lang_codes

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CUR_DIR)

dict_of_data_sets = dict()


class DataUpdating:
    @staticmethod
    def check_data():
        path, dirs, files = next(os.walk(f"{BASE_DIR}/data"))
        if len(lang_codes) != len(files):  # updating our data in case some files are lost or not downloaded
            DataUpdating.initialize_all_data()

    @staticmethod
    def get_data_from_set(lang_code):
        if lang_code not in lang_codes:
            abort(404, message='No such a language code')
        elif lang_code not in dict_of_data_sets:
            DataUpdating.update_data(lang_code)

        return dict_of_data_sets[lang_code]

    @staticmethod
    def update_data(lang_code, ):
        url = lang_codes.get(lang_code)

        try:  # if github doesn't respond, then parse saved file without downloading
            words = requests.get(url, allow_redirects=True)
            words = words.text
            with open(f'{BASE_DIR}/data/words_{lang_code}.txt', 'w') as f:
                f.write(words)
        except:
            with open(f'{BASE_DIR}/data/words_{lang_code}.txt', 'r') as words:
                words.read()
        DataUpdating._make_sets(lang_code, words)
        return dict_of_data_sets[lang_code]

    @staticmethod
    def initialize_all_data():
        for lang_code in lang_codes:
            DataUpdating.update_data(lang_code)

    @staticmethod
    def _make_sets(lang_code, words):
        bad_words = set(bw.strip("\n") for bw in words)
        dict_of_data_sets[lang_code] = bad_words
        return dict_of_data_sets[lang_code]

