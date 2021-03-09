import requests
from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

lang = 'en-US'


class TextFiltering:

    def get_from_url(self, ):
        url = "https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt"
        r = requests.get(url, allow_redirects=True)
        r = r.text
        open(f'data/words_{lang}.txt', 'w').write(r)

    def filter_text(self, text):
        special_symbols = ('!', '?', '.', ',', ':', ';', '-', '_',)

        bad_words = set(bw.strip("\n") for bw in open(f'data/words_{lang}.txt'))
        text = text.split()
        filtered_text = []
        for word in text:
            temp_val = ""
            while word.endswith(special_symbols):
                temp_val += word[-1]
                word = word[:-1]
            if word in bad_words:
                line_length = len(word)
                word = '*' * line_length
            filtered_text.append(word + temp_val)
        filtered_text = ' '.join(filtered_text)
        return {'filtered text': filtered_text}


class RequestHandler(Resource):

    def post(self):
        some_json = request.get_json()
        some_text = TextFiltering()
        try:
            return some_text.filter_text(some_json['message'])
        except KeyError:
            abort(404, message='KeyError')
        except TypeError:
            abort(415, message='Unsupported Media Type')


api.add_resource(RequestHandler, f'/api/filter-bad-words/{lang}')

if __name__ == '__main__':
    app.run()
