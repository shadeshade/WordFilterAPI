from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class RequestHandler(Resource):
    def post(self):
        pass


if __name__ == '__main__':
    app.run()
