from flask import Blueprint, request, jsonify
from database import getDB
from models.user import User

user_bp = Blueprint("user", __name__)

@user_bp.route('/user', methods = ['GET', 'POST'])
def getAndAddUser():
    if request.method == 'GET':
        email = request.args.get('email')
        if email is None:
            with getDB() as db:
                allUsers = db.query(User).all()
                userList = []
                for user in allUsers:
                    user_data = {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                    }
                    userList.append(user_data)
                return userList, 200
        
        with getDB() as db:
            existedUser = db.query(User).filter_by(email=email).first()
            if existedUser:
                userData = {
                    "id": existedUser.id,
                    "name": existedUser.name,
                    "email": existedUser.email,
                }
                return userData, 200
        return {"message": "User does not exist"}, 400
    
    elif request.method == 'POST':
        data = request.json
        newUser = User(name=data["name"], email=data["email"], password=data["password"])
        with getDB() as db:
            existedUser = db.query(User).filter_by(email=data["email"]).first()
            if existedUser:
                return {"message": "User already exists"}, 400
            db.add(newUser)
            db.commit()
            db.refresh(newUser)
        userData = {
            "id": newUser.id,
            "name": newUser.name,
            "email": newUser.email,
        }
        return userData, 201
    

    
@user_bp.route('/user/<email>', methods = ['DELETE', 'PUT'])
def deleteAndUpdateUser(email):
    if request.method == 'DELETE':
        with getDB() as db:
            existedUser = db.query(User).filter_by(email=email).first()
            if existedUser:
                db.delete(existedUser)
                db.commit()
                return {"message": "User deleted successfully"}, 200
        return {"message": "User does not exists"}, 400
    
    elif request.method == 'PUT':
        data = request.json
        with getDB() as db:
            existedUser = db.query(User).filter_by(email=email).first()
            if existedUser:
                existedUser.email = data.get("email", existedUser.email)
                existedUser.name = data.get("name", existedUser.name)
                existedUser.password = data.get("password", existedUser.password)
                db.commit()
                return {"message": "User updated successfully"}, 200
        return {"message": "User does not exists"}, 400