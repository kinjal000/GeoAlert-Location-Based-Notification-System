from flask import Blueprint
from controllers.location_controller import LocationController

# Create Blueprint
location_bp = Blueprint("location_bp", __name__)

# -----------------------------------
# Update User Location
# URL : POST /update-location
# -----------------------------------

@location_bp.route("/update-location", methods=["POST"])
def update_location():

    return LocationController.update_location()