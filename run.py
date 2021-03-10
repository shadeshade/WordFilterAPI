from flask import request
from flask_restful import Resource, abort

from app import api
from app import server
from app.filtering import TextFiltering, lang_codes
from app.scheduling import set_daily_update, scheduler


# TODO:
# 3. if passed lang is not supported, return an error
# 4. break run.py to multiple files based on style principles


def register_resource(*urls, **kwargs):
    def decorator(cls):
        api.add_resource(cls, *urls, **kwargs)
        return cls

    return decorator


@register_resource(f'/api/filter-bad-words/<lang_code>')
class RequestHandler(Resource):

    def post(self, lang_code):
        if lang_code not in lang_codes:
            abort(404, message='No such a language code')

        to_filter = TextFiltering()
        try:
            # fixme: they could send data in different format, catch exception if not json
            some_json = request.get_json()

            return to_filter.filter_text(some_json['message'], lang_code)
        except KeyError:
            abort(404, message='KeyError')
        except TypeError:
            abort(415, message='Unsupported Media Type')


if __name__ == '__main__':
    # todo: initialize set with bad words at the start
    set_daily_update()
    scheduler.start()

    server.run()
    # app.run(host="localhost", port=4201, debug=True)
