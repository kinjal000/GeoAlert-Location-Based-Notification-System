from database.mongo_db import (
    location_collection,
    geofence_collection
)


class LocationModel:

    @staticmethod
    def save_location(user_id, location):

        data = {

            "user_id": user_id,

            "location": location

        }

        location_collection.insert_one(data)

        return True

    @staticmethod
    def get_geofence(location):

        geofence = geofence_collection.find_one(

            {

                "location": {

                    "$regex": f"^{location}$",

                    "$options": "i"

                }

            }

        )

        return geofence

    @staticmethod
    def get_location_history(user_id):

        history = list(

            location_collection.find(

                {

                    "user_id": user_id

                },

                {

                    "_id": 0

                }

            )

        )

        return history