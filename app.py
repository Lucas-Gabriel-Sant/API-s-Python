from flask import Flask, jsonify
from flask_restful import Api

from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites, SiteMedia
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    app.before_request_funcs[None].remove(cria_banco)
    #linha adicional para remover o manipulador do app e fazer este código ser executado apenas na primeira requisição

    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_block_list(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payloader):
    return jsonify({"message": "You have been logged out."}), 401 # unauthorized

api.add_resource(Hoteis, '/hoteis')
#Buscar todos os hotéis através do '/hoteis'
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(SiteMedia, '/sites/media')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

if __name__ == '__main__':
    from sql_alquemy import banco
    banco.init_app(app)

    app.run(debug=True)
    #debug=True durante produção, False ou retirar debug após finalização

# http://127.0.0.1:5000/hoteis --> arquivo JSON