import os

import requests

from app.filtering import lang_codes

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CUR_DIR)


class DataUpdating:
    @staticmethod
    def check_data():
        path, dirs, files = next(os.walk(f"{BASE_DIR}/data"))
        if len(lang_codes) != len(files):  # updating our data in case some files are lost or not downloaded
            DataUpdating.update_all_data()

    @staticmethod
    def get_data(lang_code):
        url = lang_codes.get(lang_code)
        r = requests.get(url, allow_redirects=True)
        r = r.text
        with open(f'{BASE_DIR}/data/words_{lang_code}.txt', 'w') as f:
            f.write(r)
            return f

    @staticmethod
    def update_all_data():
        # todo: download into txt file, and then parse it into set
        # if github doesn't respond, then parse saved file without downloading
        for lang_code in lang_codes:
            url = lang_codes.get(lang_code)
            r = requests.get(url, allow_redirects=True)
            r = r.text
            with open(f'{BASE_DIR}/data/words_{lang_code}.txt', 'w') as f:
                f.write(r)

# bad_words = set(bw.strip("\n") for bw in open(f'{BASE_DIR}/data/words_{lang_code}.txt'))
