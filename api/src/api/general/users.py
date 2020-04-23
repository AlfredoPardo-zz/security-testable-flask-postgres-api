from flask_restplus import Resource, Namespace, fields, marshal_with
from flask import request
from datetime import timedelta

from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required,
    decode_token
)

ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRATION = timedelta(hours=12)

from database.models.general.user import User
from database import db

api = Namespace("users", description="Users")

model = api.model("users", {
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password"),
    "name": fields.String(required=True, description="User's name")
})

model_auth = api.model("users_auth", {
    "username": fields.String(required=True, description="Username"),
    "password": fields.String(required=True, description="Password")
})

@api.route('/')
class Users(Resource):
    
    @jwt_required
    @api.marshal_list_with(model)
    def get(self):
        '''Lists all Users'''
        return list(User.query.all()), 200

    @jwt_required
    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        '''Creates a new User'''
        if request.is_json:
            content = request.json
            user = User(username=content["username"], \
                password=content["password"], \
                name=content["name"])
            db.session.add(user)
            db.session.commit()
            return user, 201
        else:
            return 400

@api.route('/<string:username>')
class Users_By_Username(Resource):

    @jwt_required
    @api.marshal_with(model)
    def get(self, username):
        '''Shows a User'''
        user = User.query.filter(User.username==username).first()
        if user:
            return user, 200
        else: 
            return {}, 404

    @jwt_required
    def delete(self, username):
        '''Deletes a User'''
        
        user = User.query.filter(User.username==username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"msg": "{} has been removed.".format(username)}, 200
        else:
            return {"msg": "{} has not been found.".format(username)}, 404
    
    @jwt_required
    @api.expect(model)
    @api.marshal_with(model, code=200)
    def put(self, username):
        '''Updates a User'''
        if request.is_json:
            content = request.json
            user = User.query.filter(User.username==username).first()
            if user:
                user.password = content["password"]
                user.name = content["name"]
                db.session.add(user)
                db.session.commit()
                return user, 200
            else:
                return {}, 404
        else:
            return {}, 400


@api.route('/auth')
class Users_Auth(Resource):

    @api.expect(model_auth)
    def post(self):
        '''Authenticates a User'''
        if request.is_json:
            content = request.json
            user = User.query.filter(User.username==content["username"],\
                User.password==content["password"]).first()
            if user:
                username = user.username
                print("ACCESS_TOKEN_EXPIRATION: {}".format(ACCESS_TOKEN_EXPIRATION))
                access_token = create_access_token(identity=username, expires_delta=ACCESS_TOKEN_EXPIRATION)
                print("REFRESH_TOKEN_EXPIRATION: {}".format(REFRESH_TOKEN_EXPIRATION))
                refresh_token = create_refresh_token(identity=username, expires_delta=REFRESH_TOKEN_EXPIRATION)
                return {
                    "access_token": access_token,
                    "refresh_token" : refresh_token,
                    "username": user.username,
                    "name": user.name
                }, 200
        else:
            return 400

@api.route('/refresh_auth')
class Users_Refresh_Auth(Resource):
    
    @jwt_refresh_token_required
    @api.expect(model_auth)
    def post(self):
        '''Refreshs the Authentication Token for a User'''
        if request.is_json:
            content = request.json

            token = content.get('token')

            if token:
                refresh_token = decode_token(token)
                access_token = create_access_token(identity=refresh_token["identity"], expires_delta=ACCESS_TOKEN_EXPIRATION)
                return {"access_token": access_token}, 200
            else:
                return {"msg": "Missing token parameter.-"}, 400

        else:
            return 400

