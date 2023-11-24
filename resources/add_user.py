from flask_restful import Resource
from db import db
from models.users import User
from flask import jsonify, request

class AddUser(Resource):

    def post(self):
        data = request.get_json()

        new_user = User(username=data['username'], email=data['email'], role=data['role'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        # Send email to the newly added agent
        # send_email('Welcome to the System', 'Your username: {}\nYour password: {}'.format(data['username'], data['password']), data['email'])

        return jsonify(message='User added successfully')

    def put(self, user_id):
        user = User.query.get(user_id)
        user.is_blocked = True
        db.session.commit()
        return jsonify(message='User blocked successfully')
