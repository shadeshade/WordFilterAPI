# from flask import request
# from flask_restful import Resource, abort
#
# from app.filtering import TextFiltering, lang_codes
# from app import api
#
#
# def register_resource(*urls, **kwargs):
#     def decorator(cls):
#         api.add_resource(cls, *urls, **kwargs)
#         return cls
#
#     return decorator
#
# @register_resource(f'/api/filter-bad-words/<lang_code>')
# class RequestHandler(Resource):
#
#     def post(self, lang_code):
#         if lang_code not in lang_codes:
#             abort(404, message='No such a language code')
#
#         to_filter = TextFiltering()
#         try:
#             # fixme: they could send data in different format, catch exception if not json
#             some_json = request.get_json()
#
#             return to_filter.filter_text(some_json['message'], lang_code)
#         except KeyError:
#             abort(404, message='KeyError')
#         except TypeError:
#             abort(415, message='Unsupported Media Type')
