import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

scheduler = BackgroundScheduler()

# TODO:
# 1. update words base once a day, scheduled
# 2. pass `lang` argument through URL arguments
# 3. if passed lang is not supported, return an error
# 4. break app.py to multiple files based on style principles


lang_codes = ['en-US']


class TextFiltering:

    def get_from_url(self, ):
        url = "https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt"
        r = requests.get(url, allow_redirects=True)
        r = r.text
        # for lang in lang_codes:
        #     open(f'data/words_{lang}.txt', 'w').write(r)
        open(f'words_en-US.txt', 'w').write(r)

    def filter_text(self, text, lang):
        special_symbols = ('!', '?', '.', ',', ':', ';', '-', '_',)
        gram_endings = ('ing', 'ed', 'es', 's',)

        bad_words = set(bw.strip("\n") for bw in open(f'data/words_{lang}.txt'))

        text = text.split()
        filtered_text = []
        for word in text:
            temp_val = ""
            while word.endswith(special_symbols):  # exclude special symbols
                temp_val += word[-1]
                word = word[:-1]
            if word.endswith(gram_endings) and word not in bad_words:  # exclude grammatical endings
                for ending in gram_endings:
                    if word.endswith(ending):
                        ending_len = len(ending)
                        temp_val += word[-ending_len]
                        word = word[:-ending_len]
                        break
            if word in bad_words:
                line_length = len(word)
                word = '*' * line_length
            filtered_text.append(word + temp_val[::-1])  # add our endings back
        filtered_text = ' '.join(filtered_text)
        return {'filtered text': filtered_text}


def register_resource(*urls, **kwargs):
    def decorator(cls):
        api.add_resource(cls, *urls, **kwargs)
        return cls

    return decorator


@register_resource(f'/api/filter-bad-words/<lang_code>')
class RequestHandler(Resource):

    def post(self, lang_code):
        if lang_code not in lang_codes:
            abort(404, message='BAD NEWS')

        some_json = request.get_json()
        some_text = TextFiltering()
        try:
            return some_text.filter_text(some_json['message'], lang_code)
        except KeyError:
            abort(404, message='KeyError')
        except TypeError:
            abort(415, message='Unsupported Media Type')


# api.add_resource(RequestHandler, f'/api/filter-bad-words/{lang}',)


def set_daily_update():
    tf = TextFiltering()
    scheduler.add_job(tf.get_from_url, 'interval', hours=24)


if scheduler.state == 0:
    set_daily_update()
    scheduler.start()

if __name__ == '__main__':

    tf = TextFiltering()
    tf.get_from_url()
    app.run()


    # app.run(host="localhost", port=4201, debug=True)