import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from app.scheduling import set_daily_update, scheduler
from app.updating import initialize_all_data
from app.views import RequestHandler

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(CUR_DIR)

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

server = Flask(__name__)
api = Api(server)

if scheduler.state == 0:
    initialize_all_data()
    set_daily_update()
    scheduler.start()

api.add_resource(RequestHandler, '/api/filter-bad-words/<lang_code>')
