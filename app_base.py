from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Hoteis(Resource):
    def __init__(self):
        self.hoteis = {'hoteis': 'meus hoteis'}

    def get(self):
        return self.hoteis

    # return em JSON

api.add_resource(Hoteis, '/hoteis')
#Buscar todos os hotéis através do '/hoteis'

if __name__ == '__main__':
    app.run(debug=True)
    #debug=True durante produção, False ou retirar debug após finalização

# http://127.0.0.1:5000/hoteis --> arquivo JSON