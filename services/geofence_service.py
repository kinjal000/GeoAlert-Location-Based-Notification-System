import random
import datetime
from models.location_model import LocationModel
from models.notification_model import NotificationModel

class GeofenceService:
    TEMPLATES = {
        "MALL": [
            {"icon": "🛍️", "title": "Nykaa Flat 40% Sale Today", "desc": "Exclusive 40% flat discount on all premium cosmetics brands. Today only!", "category": "Offer"},
            {"icon": "🍔", "title": "McDonald's Combo Offer", "desc": "Buy 1 McSpicy Chicken Meal and get a regular fries free!", "category": "Offer"},
            {"icon": "🎬", "title": "PVR Ticket Wednesday Special", "desc": "All standard screen movie tickets available for just ₹199 today.", "category": "Event"},
            {"icon": "🎮", "title": "Timezone Buy 2 Get 1 Game", "desc": "Load your gaming card and get an additional credit pack bonus.", "category": "Offer"},
            {"icon": "🅿️", "title": "Parking Almost Full", "desc": "Level 1 and Level 2 parking zones are fully occupied. Divert to basement B3.", "category": "Parking"},
            {"icon": "🚗", "title": "Heavy Weekend Traffic", "desc": "High influx of vehicles near main mall gates. Expect delays of 20 mins.", "category": "Traffic"},
            {"icon": "🛒", "title": "Lifestyle End Of Season Sale", "desc": "Grab up to 50% discount on summer apparel collections.", "category": "Offer"},
            {"icon": "🏪", "title": "Food Court Happy Hours", "desc": "Get a flat 15% off on total bills across participating food stalls from 4PM-7PM.", "category": "Offer"},
            {"icon": "🚨", "title": "Fire Drill Announcement", "desc": "Routine safety assessment and evacuation checks at Zone C tomorrow morning.", "category": "Emergency"},
            {"icon": "✨", "title": "Live Music Weekend Concert", "desc": "Enjoy a soulful acoustic performance live at the central atrium from 7 PM onwards.", "category": "Event"},
            {"icon": "📱", "title": "Apple Store Launch Event", "desc": "Experience the latest flagship smartphones live with product specialists today.", "category": "Event"},
            {"icon": "👟", "title": "Nike Run Club Meetup", "desc": "Join local athletes at the flagship store entrance for the urban 5K run.", "category": "Event"},
            {"icon": "🍩", "title": "Dunkin Donuts Combo Special", "desc": "Pair any hot coffee with two classic glazed donuts for only ₹149.", "category": "Offer"},
            {"icon": "👜", "title": "Zara Premium Collection Launch", "desc": "Autumn luxury designs have arrived. First 50 shoppers get exclusive vouchers.", "category": "Offer"},
            {"icon": "⚠️", "title": "Escalator Maintenance in Progress", "desc": "Main central atrium escalators are undergoing routine checkups. Use lifts.", "category": "Emergency"}
        ],
        "AIRPORT": [
            {"icon": "✈️", "title": "Flight Delay Warning", "desc": "Intermittent technical weather clearances causing 15-30 mins adjustments on domestic sectors.", "category": "Emergency"},
            {"icon": "🚕", "title": "Cab Waiting Surcharge High", "desc": "Peak arrivals detected. Ride-hailing queues have expanded with higher wait margins.", "category": "Traffic"},
            {"icon": "🅿️", "title": "Parking Busy Notification", "desc": "Terminal 2 multi-level parking blocks are experiencing high vehicle ratios.", "category": "Parking"},
            {"icon": "🛄", "title": "Security Queue Congestion", "desc": "Security gates 3A through 4B are crowded. Total clearance time estimated at 22 mins.", "category": "Emergency"},
            {"icon": "☕", "title": "Cafe Coffee Day Airport Discount", "desc": "Present your boarding pass to redeem a flat 20% off on premium brews.", "category": "Offer"},
            {"icon": "🛂", "title": "Immigration Processing Swift", "desc": "International departure gates reporting low wait counters. Smooth passage.", "category": "Traffic"},
            {"icon": "🎒", "title": "Duty-Free Shopping Treats", "desc": "Pre-order absolute travel essentials online and save tax up to an extra 10%.", "category": "Offer"},
            {"icon": "📢", "title": "Terminal Announcement Updates", "desc": "Gate allocation alterations are now running exclusively over digital screens.", "category": "Event"},
            {"icon": "🛋️", "title": "Lounge Access Seat Limits", "desc": "Premium executive lounges are filling fast. Prior online reservation advised.", "category": "Parking"},
            {"icon": "🚙", "title": "Express Pickup Lanes Operational", "desc": "New dynamic parking zones dedicated for brief drop-offs are open at lane 4.", "category": "Traffic"},
            {"icon": "🔌", "title": "Charging Stations Check", "desc": "Free ultra-fast wireless charging hubs are fully active across seating gates 12-18.", "category": "Event"},
            {"icon": "🍽️", "title": "Fine Dining Gourmet Week", "desc": "Indulge in seasonal tasting platters before your long-haul flight.", "category": "Offer"},
            {"icon": "⛅", "title": "Clear Air Turbulence Warnings", "desc": "En-route flight paths heading east report standard minor wind patterns.", "category": "Emergency"},
            {"icon": " SIM", "title": "International SIM Desk Live", "desc": "Activate unlimited data roaming roaming card solutions directly at kiosk B.", "category": "Offer"},
            {"icon": "🚰", "title": "Sanitization Drive Active", "desc": "High safety maintenance check scheduled for central waiting lobbies.", "category": "Emergency"}
        ],
        "STATION": [
            {"icon": "🚆", "title": "Train Arrival Delay Alert", "desc": "Express line schedules running 12-15 minutes behind standard transit times.", "category": "Emergency"},
            {"icon": "🚕", "title": "Auto Rickshaw Bay Availability", "desc": "Prepaid transit zones have optimal auto numbers available for instant departures.", "category": "Traffic"},
            {"icon": "🍽️", "title": "Comesum Restaurant Combo Offer", "desc": "Get a executive lunch meal pack with free mineral water bottle for ₹120.", "category": "Offer"},
            {"icon": "🚦", "title": "Station Road Traffic Congestion", "desc": "High density vehicle lines near western exit. Avoid route if driving.", "category": "Traffic"},
            {"icon": "🅿️", "title": "Two-Wheeler Parking Available", "desc": "Ample parking spaces vacant at the designated platform 1 east structure.", "category": "Parking"},
            {"icon": "📢", "title": "Platform Alteration Notice", "desc": "Incoming long-distance express redirected from Platform 3 to Platform 5.", "category": "Emergency"},
            {"icon": "🎫", "title": "ATVM Smart Kiosks Open", "desc": "Skip the main ticketing window lines. Generate travel cards instantly via QR.", "category": "Offer"},
            {"icon": "🎒", "title": "Cloak Room Security Checks", "desc": "Luggage scanning and secure deposit services running with swift verifications.", "category": "Emergency"},
            {"icon": "🥤", "title": "Amul Milk Parlour Special", "desc": "Beat the travel heat with chilled buttermilk packs at a flat corporate price.", "category": "Offer"},
            {"icon": "WiFi", "title": "Free High-Speed RailWire Active", "desc": "Connect to open station Wi-Fi network for high-definition video streaming.", "category": "Event"},
            {"icon": "🛋️", "title": "AC Waiting Hall Capacity Status", "desc": "Seating layout inside upper lounges currently reporting 40% occupancy.", "category": "Parking"},
            {"icon": "⚠️", "title": "Foot Overbridge Maintenance", "desc": "North side stairs closed for step restoration. Please use the central ramp.", "category": "Emergency"},
            {"icon": "📚", "title": "Wheeler Book Store Magazine Sale", "desc": "Grab best-selling crime thrillers and local paperbacks at 15% discount.", "category": "Offer"},
            {"icon": "🚨", "title": "RPF Extra Patrolling Active", "desc": "Enhanced security watch team deployed to ensure late-night commuter safety.", "category": "Event"},
            {"icon": "🛄", "title": "Coolie Porter Tariffs App", "desc": "Check government-approved fixed porter luggage rates via official platform QR charts.", "category": "Offer"}
        ],
        "TOURIST": [
            {"icon": "🌊", "title": "High Tide Precautionary Alert", "desc": "Strong tidal waves expected within the next hour. Maintain a safe distance from walkways.", "category": "Emergency"},
            {"icon": "📸", "title": "Tourist Crowd Influx High", "desc": "Promenade regions experiencing dense walking masses. Keep personal items secure.", "category": "Parking"},
            {"icon": "☕", "title": "Sea-View Cafe Premium Discount", "desc": "Flash this notification to claim an artisanal cold coffee with any baked item.", "category": "Offer"},
            {"icon": "🚦", "title": "Evening Promenade Traffic Build-up", "desc": "Coastal peripheral roads facing substantial slowdowns. Leisure vehicles driving slowly.", "category": "Traffic"},
            {"icon": "🚓", "title": "Police Security Patrolling Active", "desc": "Dedicated state security checkpoints and mobile units ensuring public safety.", "category": "Emergency"},
            {"icon": "🎭", "title": "Sunset Open Street Cultural Event", "desc": "Catch local street artists and acoustic musicians performing live near the plaza.", "category": "Event"},
            {"icon": "🍦", "title": "Natural Ice Cream Treat Offer", "desc": "Buy any premium double scoop cup and enjoy the second scoop at half pricing.", "category": "Offer"},
            {"icon": "🚢", "title": "Ferry Cruise Boat Timings Normal", "desc": "Hourly harbor tour departures are operating smoothly on perfect maritime weather.", "category": "Event"},
            {"icon": "☀️", "title": "High UV Index Precaution", "desc": "Solar temperatures rising. Stay perfectly hydrated and seek immediate canopy shelter.", "category": "Emergency"},
            {"icon": "🅿️", "title": "Public Coastal Parking Full", "desc": "Main street side parking bays are entirely occupied. Utilize automated structures.", "category": "Parking"},
            {"icon": "🎨", "title": "Local Heritage Photography Walk", "desc": "Join historic archiving enthusiasts capturing iconic monumental architecture structures.", "category": "Event"},
            {"icon": "🧋", "title": "Street Food Hygiene Vouched Stalls", "desc": "Savor validated authentic local savories at certified hyper-clean vendor outlets.", "category": "Offer"},
            {"icon": "🧹", "title": "Cleanliness Drive Initiative", "desc": "Support green disposal workers keeping our marine ecosystem waste free.", "category": "Event"},
            {"icon": "🚲", "title": "Eco Bicycle Rental Hub Open", "desc": "Unlock smart tracking premium cycles for just ₹20 per hour of shoreline tracking.", "category": "Offer"},
            {"icon": "🏰", "title": "Laser Light Show Countdown", "desc": "Spectacular colorful projection Mapping over main structural facades starts at 8 PM.", "category": "Event"}
        ],
        "COLLEGE": [
            {"icon": "🎓", "title": "Annual Tech Fest Registration Open", "desc": "Compete across multiple coding hackathons, robowars, and innovative project expos.", "category": "Event"},
            {"icon": "📢", "title": "Guest AI Seminar Today", "desc": "Distinguished tech scientists talking on next-gen transformer architectures at auditorium 2.", "category": "Event"},
            {"icon": "🍔", "title": "Student Canteen Combo Deal", "desc": "Get a fresh paneer wrap, french fries, and cold beverage bottle for just ₹99.", "category": "Offer"},
            {"icon": "🚌", "title": "University Shuttle Bus Delay", "desc": "Outer traffic intersection gridlock causing a brief 10-minute shift in arrival timelines.", "category": "Traffic"},
            {"icon": "📚", "title": "Library Extended Midnight Hours", "desc": "Reading rooms and reference shelves will stay operational until 12:00 AM for semester preparation.", "category": "Parking"},
            {"icon": "💻", "title": "Coding Club Competitive Coding", "desc": "Weekly internal algorithmic sprint begins tonight at the advanced computer labs.", "category": "Event"},
            {"icon": "🔬", "title": "Innovation Lab Grants Open", "desc": "Submit prototype research designs to secure up to ₹50,000 corporate development fund.", "category": "Offer"},
            {"icon": "⚠️", "title": "Wi-Fi Server Node Upgraded", "desc": "Brief intermittent connection blips expected during hardware load balancing resets.", "category": "Emergency"},
            {"icon": "🏀", "title": "Inter-College Basketball Finals", "desc": "Cheer for the home team competing against state rivals at the sports stadium complex.", "category": "Event"},
            {"icon": "🅿️", "title": "Student Vehicle Parking Slots Free", "desc": "Ample parking configurations open at the basement structure of the engineering wing.", "category": "Parking"},
            {"icon": "👕", "title": "Merchandise Distribution Counter Open", "desc": "Collect premium event hoodies and college track shirts by producing ID cards.", "category": "Offer"},
            {"icon": "🌱", "title": "Campus Green Plantation Drive", "desc": "Help community service clubs embed organic botanical ecosystems around open lawns.", "category": "Event"},
            {"icon": "🚨", "title": "Scholarship Application Deadline", "desc": "Final window to upload academic grade sheets and household statements via the dashboard.", "category": "Emergency"},
            {"icon": "🥪", "title": "Cafe Coffee Point Snacking Special", "desc": "Flat 10% student discount active across all hot espresso configurations.", "category": "Offer"},
            {"icon": "🛑", "title": "No Vehicle Entry Zone Enforced", "desc": "Strict walking-only rules implemented at historical central quadrangle areas.", "category": "Emergency"}
        ],
        "HOSPITAL": [
            {"icon": "🚑", "title": "Emergency Evacuation Route Busy", "desc": "High critical responder movement at primary lane. Keep paths explicitly unobstructed.", "category": "Emergency"},
            {"icon": "🅿️", "title": "Visitor Parking Matrix Full", "desc": "Main grade level spaces are fully choked. Kindly head towards multi-level wing B.", "category": "Parking"},
            {"icon": "☕", "title": "Apollo Wellness Medical Store Offer", "desc": "Claim a complimentary health assessment voucher and 15% discount on lifestyle supplements.", "category": "Offer"},
            {"icon": "🚦", "title": "Front Gate Ambulance Lane Traffic", "desc": "Heavy vehicle bottlenecking outer bypass roads. Local police deploying diversions.", "category": "Traffic"},
            {"icon": "🩺", "title": "Free Public Health Screening Camp", "desc": "Walk in for blood sugar monitoring and cardiac pressure evaluations at wing 1 flat atrium.", "category": "Event"},
            {"icon": "🥛", "title": "Organic Juice & Nutrition Counter Open", "desc": "Enjoy direct cold-pressed health wellness juices formulated by expert dieticians.", "category": "Offer"},
            {"icon": "🔕", "title": "Strict Silent Zone Regulations Enforced", "desc": "Honking or noisy mechanical behavior strictly restricted inside a 500m hospital perimeter.", "category": "Emergency"},
            {"icon": "🩸", "title": "Urgent Blood Donation Campaign", "desc": "Critical rare negative blood categories needed immediately. Visit the collection unit.", "category": "Event"},
            {"icon": "😷", "title": "Mask Compliance Regulations", "desc": "Compulsory surgical mask coverage enforced across intensive wards and observation wings.", "category": "Emergency"},
            {"icon": "🧴", "title": "Sanitizer Stations Inventory Restocked", "desc": "Touchless disinfection systems are operating perfectly across all floor elevator doors.", "category": "Parking"},
            {"icon": "🛗", "title": "Bed Lift Optimization Routine", "desc": "Lifts 3 and 4 are strictly locked for patient stretcher relocation operations.", "category": "Emergency"},
            {"icon": "🧬", "title": "Advanced Medical Robotics Webinar", "desc": "Watch surgeons dissect precision surgical tech streaming directly in the main seminar hall.", "category": "Event"},
            {"icon": "💊", "title": "Generic Medicines Store Discount", "desc": "Access high-standard bio-equivalent formulas at up to 70% economical pricing cuts.", "category": "Offer"},
            {"icon": "🌿", "title": "Therapeutic Botanical Garden Open", "desc": "Take quiet restorative walks inside our beautifully designed mental healing pavilion landscape.", "category": "Event"},
            {"icon": "ℹ️", "title": "Digital OPD Tokens Active", "desc": "Track real-time specialist consultation waiting position via phone without queuing.", "category": "Offer"}
        ],
        "DEFAULT": [
            {"icon": "📍", "title": "Location Check-In Successful", "desc": "System has locked tracking updates. GeoAlert background monitoring active.", "category": "Event"},
            {"icon": "🚦", "title": "Standard Traffic Flow Operating", "desc": "Average velocities tracked at 45 km/h. No major disruptions reporting.", "category": "Traffic"},
            {"icon": "⚡", "title": "Local Area Network Synchronized", "desc": "Local cellular network nodes streaming optimal real-time communication packets.", "category": "Event"},
            {"icon": "🅿️", "title": "Street Level Parking Available", "desc": "Unrestricted parking structures observed with stable hourly vacancy rates.", "category": "Parking"},
            {"icon": "🏪", "title": "Convenience Kiosks Nearby", "desc": "Standard daily need amenities and emergency response stations mapped.", "category": "Offer"},
            {"icon": "🌤️", "title": "Stable Microclimate Checked", "desc": "Weather diagnostics report normal local ambient temperatures with minimal cloud layer.", "category": "Event"},
            {"icon": "🚨", "title": "Emergency Support Lines Active", "desc": "Dial emergency dispatch directly from dashboard widget if any assistance needed.", "category": "Emergency"},
            {"icon": "📶", "title": "High Density Public Smart Wi-Fi", "desc": "Free internet infrastructure mapped for active users across the sector.", "category": "Offer"},
            {"icon": "🚧", "title": "Minor Road Maintenance Works", "desc": "Left lanes brief narrowing observed after next block crossroads intersection.", "category": "Traffic"},
            {"icon": "🎭", "title": "Community Gathering Awareness", "desc": "Weekend neighborhood marketplace scheduled in adjacent open sports grounds.", "category": "Event"},
            {"icon": "🛍️", "title": "Retail Outlet Coupon Code", "desc": "Get a flat 5% extra cash rebate by scanning using digital localized payment tools.", "category": "Offer"},
            {"icon": "🚲", "title": "Public Bike Stations Mapping Active", "desc": "Eco micromobility ride stations show high tracking operational inventory volumes.", "category": "Parking"},
            {"icon": "💧", "title": "Drinking Water Stations Checked", "desc": "Municipal highly purified clean hydration infrastructure located near intersections.", "category": "Emergency"},
            {"icon": "🏢", "title": "Civic Administration Desk Online", "desc": "File quick region digital asset claims directly through your smartphone interface.", "category": "Offer"},
            {"icon": "🔒", "title": "High Security Patrol Index", "desc": "Active visual camera feeds and foot surveillance keeping neighborhoods safe.", "category": "Emergency"}
        ]
    }

    @staticmethod
    def classify_location(loc_name):
        name = loc_name.upper()
        if any(w in name for w in ["MALL", "SHOPPING", "PHOENIX", "R CITY", "VIVIANA", "LULU", "FORUM", "PVR", "INFINITY"]):
            return "MALL"
        if any(w in name for w in ["AIRPORT", "TERMINAL", "HELIPORT"]):
            return "AIRPORT"
        if any(w in name for w in ["STATION", "RAILWAY", "METRO", "TERMINUS"]):
            return "STATION"
        if any(w in name for w in ["BEACH", "MARINE DRIVE", "GATEWAY", "TOURIST", "PROMENADE", "FORT"]):
            return "TOURIST"
        if any(w in name for w in ["COLLEGE", "UNIVERSITY", "CAMPUS", "INSTITUTE", "SCHOOL"]):
            return "COLLEGE"
        if any(w in name for w in ["HOSPITAL", "CLINIC", "MEDICAL", "CARE"]):
            return "HOSPITAL"
        return "DEFAULT"

    @staticmethod
    def process_location(user_id, location_name):
        # 1. Save standard location info via MongoDB LocationModel
        LocationModel.save_location(user_id, location_name)
        
        # 2. Extract Category key
        cat_key = GeofenceService.classify_location(location_name)
        pool = GeofenceService.TEMPLATES[cat_key]
        
        # 3. Randomly choose 3 completely distinct templates to avoid repetition
        chosen_templates = random.sample(pool, min(3, len(pool)))
        
        saved_notifications = []
        current_time_str = datetime.datetime.now().strftime("%I:%M %p")
        
        for t in chosen_templates:
            # Build intelligent message map structure
            msg_payload = {
                "icon": t["icon"],
                "title": t["title"],
                "description": t["desc"],
                "location": location_name,
                "time": current_time_str,
                "status": "Active",
                "category": t["category"]
            }
            
            # Save into notification logs collection via NotificationModel
            NotificationModel.save_notification(user_id, msg_payload)
            saved_notifications.append(msg_payload)

        # 4. Synthesize complete context metadata cards block structure
        weather_conditions = ["Clear Sky, 29°C", "Partly Cloudy, 27°C", "Humid, 31°C", "Breezy, 26°C", "Overcast, 25°C"]
        traffic_levels = ["Smooth - 10 min delay", "Moderate - 25 min delay", "Heavy Congestion - 45 min delay", "Bumper to Bumper"]
        safety_indices = ["High Safety Level", "Excellent Patrol Index", "Moderate Caution Advised", "Secure Zone Status"]

        context_cards = {
            "traffic_status": random.choice(traffic_levels),
            "nearby_offer": next((n["title"] for n in saved_notifications if n["category"] == "Offer"), "Special Local Rebate 10% Active"),
            "emergency_alert": next((n["title"] for n in saved_notifications if n["category"] == "Emergency"), "All systems operating normally."),
            "nearby_event": next((n["title"] for n in saved_notifications if n["category"] == "Event"), "Weekly Neighborhood Market Gathering"),
            "parking_status": random.choice(["Available Level 1-3", "85% Full - Use Basement", "Ample Open Parking Open", "Almost Full"]),
            "crowd_status": random.choice(["Normal Commerical Density", "Highly Crowded Peak Hours", "Low Leisure Footfall", "Moderate Gathering"]),
            "weather": random.choice(weather_conditions),
            "distance": f"{round(random.uniform(0.8, 12.5), 1)} km",
            "arrival_time": f"{random.randint(4, 35)} mins",
            "safety_level": random.choice(safety_indices)
        }

        return {
            "status": True,
            "inside_geofence": True,
            "location": location_name,
            "notifications": saved_notifications,
            "context_cards": context_cards
        }