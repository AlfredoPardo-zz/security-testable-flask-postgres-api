from flask_restplus import Resource, Namespace, fields
from flask import request
from uuid import uuid4
from database.models.cloud.cloud_account import CloudAccount
from database.models.cloud.cloud_provider import CloudProvider
from database.models.general.customer import Customer
from database import db
# Included Models for Marshalling
from api.general.customers import model as cs
from api.cloud.cloud_providers import model as cp

api = Namespace('cloud_accounts', description='Cloud Accounts')

model = api.model('cloud_accounts', {
    'uid': fields.String(required=True, description='Cloud Account ID'),
    'name': fields.String(required=True, description='Cloud Account Name'),
    'customer': fields.Nested(cs, "Customer"),
    'cloud_provider': fields.Nested(cp, "Cloud Provider")
})

model_cu = api.model('cloud_accounts_cu', {
    'uid': fields.String(required=True, description='Cloud Account ID'),
    'name': fields.String(required=True, description='Cloud Account Name'),
    'customer_uid': fields.String(required=True, description='Customer UID'),
    'cloud_provider_uid': fields.String(required=True, description='Cloud Provider UID')
})

@api.route('/')
class Cloud_Accounts(Resource):

    @api.marshal_list_with(model)
    def get(self):
        '''Lists all Cloud Accounts'''
        return list(CloudAccount.query.all()), 200

    @api.expect(model_cu)
    @api.marshal_with(model_cu, code=201)
    def post(self):
        '''Creates a new Cloud Account'''

        if request.is_json:
            content = request.json

            uid = str(uuid4())
            cloud_account = CloudAccount(uid=uid, \
                name=content["name"], \
                customer_uid=content["customer_uid"], \
                cloud_provider_uid=content["cloud_provider_uid"])
            
            db.session.add(cloud_account)
            db.session.commit()
            
            return cloud_account, 201

        else:
            return 400

@api.route('/<string:uid>')
class Cloud_Accounts_By_UID(Resource):

    @api.marshal_with(model)
    def get(self, uid):
        '''Shows a Cloud Account'''
        cloud_account = CloudAccount.query.filter(CloudAccount.uid==uid).first()

        if cloud_account:
            return cloud_account, 200
        else:
            return {}, 404

    def delete(self, uid):
        '''Deletes a Cloud Account'''
        
        cloud_account = CloudAccount.query.filter(CloudAccount.uid==uid).first()
        
        if cloud_account:
            db.session.delete(cloud_account)
            db.session.commit()
            return {"msg": "{} has been removed.".format(uid)}, 200
        else:
            return {"msg": "{} has not been found.".format(uid)}, 404
        
    @api.expect(model_cu)
    @api.marshal_with(model_cu, code=200)
    def put(self, uid):
        '''Updates a Cloud Account'''
        if request.is_json:
            content = request.json
            cloud_account = CloudAccount.query.filter(CloudAccount.uid==uid).first()
            if cloud_account:

                cloud_account.name = content["name"]
                cloud_account.customer_uid = content["customer_uid"]
                cloud_account.cloud_provider_uid = content["cloud_provider_uid"]
                db.session.add(cloud_account)
                db.session.commit()

                return cloud_account, 200
            
            else:
            
                return {}, 404
        
        else:
            
            return {}, 400