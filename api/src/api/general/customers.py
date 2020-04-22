from flask_restplus import Resource, Namespace, fields, marshal_with
from flask import request
from uuid import uuid4
from database.models.general.customer import Customer
from database import db

api = Namespace('customers', description='Customers')

model = api.model('customers', {
    'uid': fields.String(required=True, description='Customer ID'),
    'name': fields.String(required=True, description='Customer Name')
})

@api.route('/')
class Customers(Resource):
   
    @api.marshal_list_with(model)
    def get(self):
        '''Lists all Customers'''
        return list(Customer.query.all()), 200

    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        '''Creates a new Customer'''
        if request.is_json:
            content = request.json
            uid = str(uuid4())
            customer = Customer(uid=uid, name=content["name"])
            db.session.add(customer)
            db.session.commit()
            return customer, 201
        else:
            return 400

@api.route('/<string:uid>')
class Customers_By_UID(Resource):

    @api.marshal_list_with(model)
    def get(self, uid):
        '''Shows a Customer'''
        customer = Customer.query.filter(Customer.uid==uid).first()

        if customer:
            return customer, 200
        else: 
            return {}, 404

    def delete(self, uid):
        '''Deletes a Customer'''
        customer = Customer.query.filter(Customer.uid==uid).first()
        
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return {"msg": "{} has been removed.".format(uid)}, 200
        else:
            return {"msg": "{} has not been found.".format(uid)}, 404
        
    @api.expect(model)
    @api.marshal_with(model, code=200)
    def put(self, uid):
        '''Updates a Customer'''
        if request.is_json:
            content = request.json
            customer = Customer.query.filter(Customer.uid==uid).first()
            if customer:
                customer.name = content["name"]
                db.session.add(customer)
                db.session.commit()
                return customer, 200
            else:
                return {}, 404
        else:
            return {}, 400