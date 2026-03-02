from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade

path_params = reqparse.RequestParser()
path_params.add_argument('estado', type=str, location='args')
path_params.add_argument('ranking_min', type=float, location='args')
path_params.add_argument('ranking_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=float, location='args')
path_params.add_argument('offset', type=float, location='args')


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('estado'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'ranking': linha[2],
                'diaria': linha[3],
                'estado': linha[4],
                'site_id': linha[5]
            })

        return {'hoteis': hoteis}
    # return em JSON

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str,  required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('ranking', type=float,  required=True, help="The field 'ranking' cannot be left blank.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('estado')
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel nedds to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Not found'}, 404  # http para não encontrado

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id "{}" already exists.'.format(hotel_id)}, 400 #Bad request (requisição errada)

        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)

        """novo_hotel = hotel_objeto.json()
        # novo_hotel = {'hotel_id': hotel_id, **dados} utilizando kwargs para simplificar o código
        hoteis.append(novo_hotel)
        return novo_hotel, 200 # http para sucesso"""

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be  associated to a valid site_id.'}, 400

        try:
            hotel_objeto.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying save hotel.'}, 500 # Internal Server Error
        return hotel_objeto.json()

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        """novo_hotel = hotel_objeto.json()
        # novo_hotel = {'hotel_id': hotel_id, **dados} #utilizando kwargs para simplificar o código"""
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel_objeto = HotelModel(hotel_id, **dados)
        try:
            hotel_objeto.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying save hotel.'}, 500 # Internal Server Error
        return hotel_objeto.json(), 201 # http para created criado

    @jwt_required()
    def delete(self, hotel_id):
        """global hoteis
        # a variável hoteis a seguir irá ser definida como a mesma criado no início do código
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]"""

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying delete hotel.'}, 500  # Internal Server Error
            return {'message': 'Hotel deleted.'}
        return{'message': 'Hotel not found.'}, 404