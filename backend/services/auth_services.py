from backend import db
from backend.models import User,Role
from flask_jwt_extended import create_access_token 

def register_user(data):

    existing_user=User.query.filter(email=data["email"]).first()

    if existing_user:
        return {"message":"Email already exists"},400

    user=User(
        username=data['username']
        email=data['email']
        role=Role.Trekker
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return {"message":"registeration successful"} , 201





def login_user(data):

    user=User.query.filter_by(email=data['email'],username=data['username']).first()

    if not user:
        return {"message" :"Invalid Email or username"} , 401

    if not user.check_password(data['password']):
        return {"message":"Wrong Password"} , 401

    access_token =create_access_token(identity=user.id,additional_claims={"role":user.role.value})


    return {"access_token":access_token,
            "role":user.role.value} , 200


#for future:
# def change_password():
# def refresh_token():