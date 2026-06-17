from flask import request, jsonify
from services.geofence_service import GeofenceService


class LocationController:

    @staticmethod
    def update_location():

        try:

            data = request.get_json()

            user_id = data.get("user_id")
            location = data.get("location")

            if not user_id or not location:

                return jsonify({
                    "status": False,
                    "message": "User ID and Location are required"
                }), 400

            result = GeofenceService.process_location(
                user_id,
                location
            )

            return jsonify(result), 200

        except Exception as e:

            return jsonify({
                "status": False,
                "message": str(e)
            }), 500
        