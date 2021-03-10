import os

from flask import Flask
from flask_restful import Api
#
# from app.filtering import TextFiltering
# from app.scheduling import set_daily_update, scheduler

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(CUR_DIR)

server = Flask(__name__)
api = Api(server)
