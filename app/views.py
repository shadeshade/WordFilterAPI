from flask import request
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest

from app.filtering import dispatch_filtering_class
from app.updating import SOURCES_BY_LANG


class RequestHandler(Resource):
    def post(self, lang_code):
        if lang_code not in SOURCES_BY_LANG:
            abort(404, message='No such a language code')

        to_filter = dispatch_filtering_class(lang_code)
        try:
            some_json = request.get_json()
            result = to_filter.filter_text(some_json['message'])
            return {'filtered text': result}
        except KeyError:
            abort(404, message='KeyError')
        except TypeError:
            abort(415, message='Unsupported Media Type')
        except BadRequest:
            abort(400, message='Bad Request')
