from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
import json

db = SQLAlchemy()

def reset_database(app):
    with app.app_context():
        from database.models.general.customer import Customer
        from database.models.general.user import User
        from database.models.cloud.cloud_provider import CloudProvider
        from database.models.cloud.cloud_account import CloudAccount
        from uuid import uuid4

        with open("data/initial_data.json") as fr:
            initial_data = json.loads(fr.read())

        db.drop_all()
        db.create_all()

        for dcustomer in initial_data["customers"]:
            
            uid = str(uuid4())
            customer = Customer(uid=uid,\
                name=dcustomer["name"])
            db.session.add(customer)
            db.session.commit()

            # This saves the last inserted customer_uid
            customer_uid = customer.uid

        for dcloud_provider in initial_data["cloud_providers"]:
            uid = str(uuid4())
            cloud_provider = CloudProvider(uid=uid,\
                name=dcloud_provider["name"], \
                abbreviation=dcloud_provider["abbreviation"])
            db.session.add(cloud_provider)
            db.session.commit()
            
            # This saves the last inserted cloud_provider_uid
            cloud_provider_uid = cloud_provider.uid


        for dcloud_account in initial_data["cloud_accounts"]:
            uid = str(uuid4())

            # This takes customer_uid and cloud_provider_uid recently inserted
            cloud_account = CloudAccount(uid=uid, \
                name=dcloud_account["name"], \
                customer_uid=customer_uid, \
                cloud_provider_uid=cloud_provider_uid)
            db.session.add(cloud_account)
            db.session.commit()

        hashing = Hashing()
        hashing_salt = initial_data["hashing_salt"]
        
        for dcloud_account in initial_data["users"]:

            hashed_password = hashing.hash_value(dcloud_account["password"], salt=hashing_salt)

            user = User(username=dcloud_account["username"], \
                password=hashed_password, \
                name=dcloud_account["name"])
            db.session.add(user)
            db.session.commit()

