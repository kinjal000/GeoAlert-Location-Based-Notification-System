from flask import Flask, render_template

from routes.user_routes import user_bp
from routes.location_routes import location_bp
from routes.notification_routes import notification_bp

app = Flask(__name__)

# Register Blueprints

app.register_blueprint(user_bp)

app.register_blueprint(location_bp)

app.register_blueprint(notification_bp)


# -------------------------
# Login Page
# -------------------------

@app.route("/")
def home():

    return render_template("login.html")


# -------------------------
# Register Page
# -------------------------

@app.route("/register-page")
def register_page():

    return render_template("register.html")


# -------------------------
# Dashboard
# -------------------------

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# -------------------------
# Profile
# -------------------------

@app.route("/profile")
def profile():

    return render_template("profile.html")


# -------------------------
# Map
# -------------------------

@app.route("/map")
def map_page():

    return render_template("map.html")


# -------------------------
# Notifications
# -------------------------

@app.route("/notifications")
def notifications():

    return render_template("notifications.html")


if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5001

    )