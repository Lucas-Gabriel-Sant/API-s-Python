from flask_restful import Resource
from models.site import SiteModel
import sqlite3
from resources.filtros import consulta_media_site

class SiteMedia(Resource):
    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        resultado = cursor.execute(consulta_media_site)

        sites = []
        for linha in resultado:
            sites.append({
                'site_id': linha[0],
                'url': linha[1],
                'qntdd_hoteis': linha[2],
                'media_ranking': linha[3]
            })

        return {'sites': sites}

class Sites(Resource):
    def get(self):
        return {'site': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):

    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found.'}, 404 # not found

    def post(self, url):
        if SiteModel.find_site(url):
            return {"message": "The site '{}' already exists.".format(url)}, 400 # bad request
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'An internal error ocurred trying to create a new site.'}, 500
        return site.json()

    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}
        return {'message': 'Site not found.'}, 404  # not found
