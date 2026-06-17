from flask import request, jsonify
from services.user_service import UserService


class UserController:

    @staticmethod
    def register():

        try:

            data = request.get_json()

            full_name = data.get("full_name")
            email = data.get("email")
            password = data.get("password")
            phone = data.get("phone")

            if not full_name or not email or not password or not phone:

                return jsonify({
                    "status": False,
                    "message": "All fields are required"
                }), 400

            result = UserService.register_user(
                full_name,
                email,
                password,
                phone
            )

            return jsonify(result)

        except Exception as e:

            return jsonify({
                "status": False,
                "message": str(e)
            }), 500

    @staticmethod
    def login():

        try:

            data = request.get_json()

            email = data.get("email")
            password = data.get("password")

            if not email or not password:

                return jsonify({
                    "status": False,
                    "message": "Email and Password required"
                }), 400

            result = UserService.login_user(
                email,
                password
            )

            return jsonify(result)

        except Exception as e:

            return jsonify({
                "status": False,
                "message": str(e)
            }), 500