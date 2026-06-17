from database.mysql_db import get_mysql_connection


class UserModel:

    @staticmethod
    def create_user(full_name, email, password, phone):

        connection = get_mysql_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO users
        (full_name, email, password, phone)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                full_name,
                email,
                password,
                phone
            )
        )

        connection.commit()

        cursor.close()

        connection.close()

    @staticmethod
    def get_user_by_email(email):

        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM users
        WHERE email=%s
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        connection.close()

        return user

    @staticmethod
    def get_user_by_id(user_id):

        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM users
        WHERE user_id=%s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()

        connection.close()

        return user