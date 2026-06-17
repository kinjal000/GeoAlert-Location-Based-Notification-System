# 📍 GeoAlert - Location Based Notification System

---

# 1. Project Overview

GeoAlert is a Location-Based Notification System developed using Python Flask, MySQL, and MongoDB. The project is designed to simulate a real-world geofencing application that provides users with nearby offers, traffic alerts, emergency notifications, and event updates based on their searched or simulated location.

The application allows users to register, log in, search for locations, view an interactive map, receive dynamic notifications, and maintain a history of searched locations. It demonstrates key System Design concepts such as geospatial processing, layered architecture, REST APIs, hybrid database integration, and notification management.

---

# 2. Setup Instructions

## Step 1: Clone the Repository

```bash
git clone https://github.com/kinjal000/GeoAlert-Location-Based-Notification-System.git
```

## Step 2: Open the Project Folder

```bash
cd GeoAlert
```

## Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

## Step 4: Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

## Step 6: Configure MySQL

- Create a database named **geoalert_db**
- Execute the SQL script to create:
  - users
  - notification_preferences
  - event_logs

## Step 7: Configure MongoDB

Create a database named:

```
geoalert
```

Create the following collections:

- geofences
- location_history
- notification_logs

## Step 8: Update Database Configuration

Open the configuration file and update:

- MySQL Host
- Username
- Password
- Database Name
- MongoDB Connection URL

according to your local system.

---

# 3. Dependencies

The project uses the following Python libraries:

```
Flask==3.1.3
flask-cors==6.0.5
PyMySQL==1.2.0
pymongo==4.17.0
Werkzeug==3.1.8
Jinja2==3.1.6
MarkupSafe==3.0.3
click==8.4.1
blinker==1.9.0
itsdangerous==2.2.0
dnspython==2.8.0
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 4. Execution Steps

## Start MySQL Server

Ensure the MySQL service is running.

## Start MongoDB Server

Ensure MongoDB Compass or MongoDB Server is running.

## Run the Flask Application

```bash
python app.py
```

The application will start on:

```
http://127.0.0.1:5001
```

## Open the Browser

Visit:

```
http://127.0.0.1:5001
```

## Application Workflow

1. Register a new account.
2. Login using your credentials.
3. Access the Dashboard.
4. Search for any location.
5. View the interactive map.
6. Receive simulated nearby notifications.
7. Check notification history.
8. View your profile information.
9. Logout securely.

---

# 5. Additional Project Details

## Project Title

**GeoAlert – Location Based Notification System**

## Technology Stack

- Python
- Flask
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- MySQL
- MongoDB
- Leaflet Maps
- OpenStreetMap

## Architecture

The project follows a layered architecture:

```
User Interface
       ↓
Routes
       ↓
Controllers
       ↓
Services
       ↓
Models
       ↓
MySQL & MongoDB
```

## Key Features

- User Authentication
- Interactive Dashboard
- Location Search
- Interactive Map
- Geofence Simulation
- Dynamic Notifications
- Location History Tracking
- Notification History
- User Profile Management
- Hybrid Database Design

## System Design Concepts Implemented

- Layered Architecture
- REST API Design
- Geofencing
- SQL and NoSQL Integration
- Event Logging
- Notification Engine
- Modular Programming
- Separation of Concerns
- Scalability-Oriented Design

## Future Enhancements

- Real GPS Tracking
- Firebase Push Notifications
- Google Maps API Integration
- AI-Based Smart Recommendations
- Real-Time Traffic Data
- Weather Alerts
- Admin Dashboard
- Cloud Deployment
- Microservices Architecture

This project was developed as part of the **System Design Final Evaluation** to demonstrate practical implementation of location-aware services, database integration, and scalable application architecture using Python and Flask.

                                    +----------------------+
                                    |        User          |
                                    | (Web Browser Client) |
                                    +----------+-----------+
                                               |
                                               |
                                               v
                                +------------------------------+
                                |      Frontend (HTML/CSS)     |
                                | Bootstrap + JavaScript       |
                                +--------------+---------------+
                                               |
                                 HTTP Request / Response
                                               |
                                               v
                             +----------------------------------+
                             |          Flask Application       |
                             |             app.py              |
                             +----------------+-----------------+
                                              |
                     -------------------------------------------------
                     |                     |                         |
                     |                     |                         |
                     v                     v                         v

          +------------------+   +-------------------+   +----------------------+
          |   User Routes    |   |  Location Routes  |   | Notification Routes  |
          +--------+---------+   +---------+---------+   +----------+-----------+
                   |                       |                         |
                   |                       |                         |
                   v                       v                         v

        +--------------------+  +----------------------+  +----------------------+
        | User Controller    |  | Location Controller  |  | Notification Control |
        +---------+----------+  +----------+-----------+  +----------+-----------+
                  |                        |                         |
                  |                        |                         |
                  v                        v                         v

        +--------------------+  +----------------------+  +----------------------+
        |  User Service      |  |  Geofence Service    |  | Notification Service |
        +---------+----------+  +----------+-----------+  +----------+-----------+
                  |                        |                         |
                  |                        |                         |
                  |          +-------------+-------------+           |
                  |          |                           |           |
                  |          |   Geofence Evaluation     |           |
                  |          | Dynamic Notification      |           |
                  |          | Location Processing       |           |
                  |          +-------------+-------------+           |
                  |                        |                         |
                  |                        |                         |
                  v                        v                         v

        +--------------------+  +----------------------+  +----------------------+
        |    User Model      |  |   Location Model     |  | Notification Model   |
        +---------+----------+  +----------+-----------+  +----------+-----------+
                  |                        |                         |
                  |                        |                         |
        ---------------------              |          --------------------------
        |                   |              |          |                        |
        v                   v              v          v                        v

+----------------+   +----------------+   +----------------+     +----------------------+
| MySQL Database |   | users table    |   | MongoDB        |     | notification_logs    |
| geoalert_db    |   | preferences    |   | geofences      |     | location_history     |
| event_logs     |   | event_logs     |   | location data  |     | geofence data        |
+----------------+   +----------------+   +----------------+     +----------------------+
                                               |
                                               |
                                               v

                           +----------------------------------------+
                           |      Dynamic Notification Engine       |
                           | Offer Alerts                           |
                           | Traffic Alerts                         |
                           | Emergency Alerts                       |
                           | Event Notifications                    |
                           +----------------+-----------------------+
                                            |
                                            |
                                            v

                      +---------------------------------------------+
                      |         Dashboard / Notification Page       |
                      | Latest Alerts                              |
                      | Notification History                       |
                      | User Interface Update                      |
                      +---------------------------------------------+