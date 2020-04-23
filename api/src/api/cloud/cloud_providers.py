from flask_restplus import Resource, Namespace, fields
from flask import request
from flask_jwt_extended import jwt_required
from uuid import uuid4
from database.models.cloud.cloud_provider import CloudProvider
from database import db

api = Namespace('cloud_providers', description='Cloud Providers')

model = api.model('cloud_providers', {
    'uid': fields.String(required=True, description='Cloud Provider ID'),
    'name': fields.String(required=True, description='Cloud Provider Name'),
    'abbreviation': fields.String(required=True, description='Cloud Provider Abbreviation')
})

@api.route('/')
class Cloud_Providers(Resource):
    
    @jwt_required
    @api.marshal_list_with(model)
    def get(self):
        '''Lists all Cloud Providers'''       
        return list(CloudProvider.query.all()), 200

    @jwt_required
    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        '''Creates a new Cloud Provider'''

        if request.is_json:
            content = request.json

            uid = str(uuid4())
            cloud_provider = CloudProvider(uid=uid, \
                name=content["name"], abbreviation=content["abbreviation"])
            db.session.add(cloud_provider)
            db.session.commit()
            return cloud_provider, 201
        else:
            return 400

@api.route('/<string:uid>')
class Cloud_Providers_By_UID(Resource):

    @jwt_required
    @api.marshal_with(model)
    def get(self, uid):
        '''Shows a Cloud Provider'''
        cloud_provider = CloudProvider.query.filter(CloudProvider.uid==uid).first()

        if cloud_provider:
            return cloud_provider, 200
        else:
            return {}, 404

    @jwt_required
    def delete(self, uid):
        '''Deletes a Cloud Provider'''
        
        cloud_provider = CloudProvider.query.filter(CloudProvider.uid==uid).first()
        
        if cloud_provider:
            db.session.delete(cloud_provider)
            db.session.commit()
            return {"msg": "{} has been removed.".format(uid)}, 200
        else:
            return {"msg": "{} has not been found.".format(uid)}, 404

    @jwt_required
    @api.expect(model)
    @api.marshal_with(model, code=200)
    def put(self, uid):
        '''Updates a Cloud Provider'''
        if request.is_json:
            content = request.json
            cloud_provider = CloudProvider.query.filter(CloudProvider.uid==uid).first()
            if cloud_provider:
                cloud_provider.name = content["name"]
                cloud_provider.abbreviation = content["abbreviation"]
                db.session.add(cloud_provider)
                db.session.commit()
                return cloud_provider, 200
            else:
                return {}, 404
        else:
            return {}, 400