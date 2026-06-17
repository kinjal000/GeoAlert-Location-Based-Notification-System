import math


class Distance:

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):

        # Radius of Earth in KM
        radius = 6371

        dlat = math.radians(lat2 - lat1)

        dlon = math.radians(lon2 - lon1)

        a = (

            math.sin(dlat / 2) ** 2

            + math.cos(math.radians(lat1))

            * math.cos(math.radians(lat2))

            * math.sin(dlon / 2) ** 2

        )

        c = 2 * math.atan2(

            math.sqrt(a),

            math.sqrt(1 - a)

        )

        distance = radius * c

        return round(distance, 2)

