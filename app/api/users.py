from flask import jsonify, request
from app.models import User
from . import api
from .. import db
import json


class User_Routes():
    @api.route("/new_user", methods=["POST"])
    def new_user():
        user = User.from_json(request.json)
        db.session.add(user)
        db.session.commit()

        return {"message": "New user created successfully"}

    @api.get("/view_users")
    def view_users():
        users = User.query.all()
        if not users:
            return {"message": "No users to display"}
        else:
            users_list = []
            for user in users:
                users_list.append(user.to_json())
        return jsonify(users_list)

    @api.get("/view_user/<int:user_id>")
    def view_user(user_id):
        user = User.query.get_or_404(user_id)
        if not user:
            return {"message": f"User of id {user_id} not found."}
        return jsonify(user.to_json())