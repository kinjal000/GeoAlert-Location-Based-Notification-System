from models.user_model import UserModel


class UserService:

    @staticmethod
    def register_user(full_name, email, password, phone):

        existing_user = UserModel.get_user_by_email(email)

        if existing_user:

            return {
                "status": False,
                "message": "Email already registered"
            }

        UserModel.create_user(
            full_name,
            email,
            password,
            phone
        )

        return {
            "status": True,
            "message": "Registration Successful"
        }

    @staticmethod
    def login_user(email, password):

        user = UserModel.get_user_by_email(email)

        if not user:

            return {
                "status": False,
                "message": "User not found"
            }

        if user["password"] != password:

            return {
                "status": False,
                "message": "Invalid Password"
            }

        return {

            "status": True,

            "message": "Login Successful",

            "user": {

                "user_id": user["user_id"],

                "full_name": user["full_name"],

                "email": user["email"],

                "phone": user["phone"]

            }

        }