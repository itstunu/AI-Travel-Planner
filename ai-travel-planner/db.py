# db.py - No database needed! Just hardcoded data

class Database:
    def __init__(self):
        print("Using hardcoded data (no database)")
    
    def get_cities(self):
        """Return hardcoded cities"""
        return [
            {'id': 1, 'name': 'Dhaka'},
            {'id': 2, 'name': 'Chittagong'},
            {'id': 3, 'name': 'Sylhet'},
            {'id': 4, 'name': 'Rajshahi'},
            {'id': 5, 'name': 'Khulna'},
            {'id': 6, 'name': 'Barisal'},
            {'id': 7, 'name': 'Comilla'},
            {'id': 8, 'name': 'Narayanganj'},
            {'id': 9, 'name': 'Mymensingh'},
            {'id': 10, 'name': 'Rangpur'},
            {'id': 11, 'name': 'Jessore'},
            {'id': 12, 'name': "Cox's Bazar"},
            {'id': 13, 'name': 'Tangail'},
            {'id': 14, 'name': 'Bogra'},
            {'id': 15, 'name': 'Dinajpur'},
            {'id': 16, 'name': 'Pabna'},
            {'id': 17, 'name': 'Noakhali'},
            {'id': 18, 'name': 'Faridpur'},
            {'id': 19, 'name': 'Sirajganj'},
            {'id': 20, 'name': 'Kushtia'}
        ]
    
    def get_routes(self):
        """Return hardcoded routes"""
        return [
            {'source': 'Dhaka', 'destination': 'Chittagong', 'cost': 450.00, 'time': 240, 'distance': 250, 'rating': 4.5},
            {'source': 'Chittagong', 'destination': "Cox's Bazar", 'cost': 250.00, 'time': 120, 'distance': 150, 'rating': 4.8},
            {'source': 'Dhaka', 'destination': 'Sylhet', 'cost': 350.00, 'time': 180, 'distance': 200, 'rating': 4.3},
            {'source': 'Sylhet', 'destination': "Cox's Bazar", 'cost': 400.00, 'time': 300, 'distance': 350, 'rating': 4.0},
            {'source': 'Dhaka', 'destination': 'Rajshahi', 'cost': 300.00, 'time': 180, 'distance': 220, 'rating': 4.2},
            {'source': 'Rajshahi', 'destination': 'Khulna', 'cost': 280.00, 'time': 150, 'distance': 180, 'rating': 4.1},
            {'source': 'Khulna', 'destination': 'Barisal', 'cost': 200.00, 'time': 120, 'distance': 130, 'rating': 4.4},
            {'source': 'Barisal', 'destination': 'Dhaka', 'cost': 320.00, 'time': 180, 'distance': 210, 'rating': 4.3},
            {'source': 'Dhaka', 'destination': 'Comilla', 'cost': 200.00, 'time': 100, 'distance': 120, 'rating': 4.6},
            {'source': 'Comilla', 'destination': 'Chittagong', 'cost': 300.00, 'time': 150, 'distance': 170, 'rating': 4.5},
            {'source': 'Dhaka', 'destination': 'Narayanganj', 'cost': 100.00, 'time': 45, 'distance': 30, 'rating': 4.7},
            {'source': 'Narayanganj', 'destination': 'Comilla', 'cost': 180.00, 'time': 90, 'distance': 100, 'rating': 4.4},
            {'source': 'Dhaka', 'destination': 'Mymensingh', 'cost': 150.00, 'time': 80, 'distance': 100, 'rating': 4.5},
            {'source': 'Mymensingh', 'destination': 'Tangail', 'cost': 180.00, 'time': 100, 'distance': 110, 'rating': 4.3},
            {'source': 'Dhaka', 'destination': 'Tangail', 'cost': 200.00, 'time': 120, 'distance': 140, 'rating': 4.2},
            {'source': 'Tangail', 'destination': 'Sirajganj', 'cost': 220.00, 'time': 130, 'distance': 150, 'rating': 4.0},
            {'source': 'Sirajganj', 'destination': 'Pabna', 'cost': 150.00, 'time': 80, 'distance': 90, 'rating': 4.3},
            {'source': 'Pabna', 'destination': 'Rajshahi', 'cost': 200.00, 'time': 100, 'distance': 120, 'rating': 4.2},
            {'source': 'Rangpur', 'destination': 'Dinajpur', 'cost': 150.00, 'time': 80, 'distance': 90, 'rating': 4.1},
            {'source': 'Dinajpur', 'destination': 'Bogra', 'cost': 200.00, 'time': 120, 'distance': 130, 'rating': 4.2},
            {'source': 'Bogra', 'destination': 'Rajshahi', 'cost': 180.00, 'time': 100, 'distance': 120, 'rating': 4.3},
            {'source': 'Jessore', 'destination': 'Khulna', 'cost': 120.00, 'time': 60, 'distance': 70, 'rating': 4.6},
            {'source': 'Khulna', 'destination': 'Barisal', 'cost': 250.00, 'time': 150, 'distance': 160, 'rating': 4.4},
            {'source': 'Dhaka', 'destination': 'Khulna', 'cost': 550.00, 'time': 300, 'distance': 350, 'rating': 4.0},
            {'source': 'Dhaka', 'destination': 'Barisal', 'cost': 400.00, 'time': 240, 'distance': 280, 'rating': 4.1},
            {'source': 'Chittagong', 'destination': 'Noakhali', 'cost': 180.00, 'time': 90, 'distance': 100, 'rating': 4.3},
            {'source': 'Noakhali', 'destination': 'Comilla', 'cost': 220.00, 'time': 120, 'distance': 140, 'rating': 4.2},
            {'source': 'Rajshahi', 'destination': 'Pabna', 'cost': 160.00, 'time': 80, 'distance': 90, 'rating': 4.4},
            {'source': 'Khulna', 'destination': 'Jessore', 'cost': 130.00, 'time': 70, 'distance': 80, 'rating': 4.5},
            {'source': 'Barisal', 'destination': 'Faridpur', 'cost': 250.00, 'time': 150, 'distance': 160, 'rating': 4.2},
            {'source': 'Faridpur', 'destination': 'Dhaka', 'cost': 280.00, 'time': 160, 'distance': 180, 'rating': 4.3},
            {'source': 'Mymensingh', 'destination': 'Rangpur', 'cost': 250.00, 'time': 150, 'distance': 160, 'rating': 4.1},
            {'source': 'Rangpur', 'destination': 'Rajshahi', 'cost': 220.00, 'time': 130, 'distance': 150, 'rating': 4.2},
            {'source': 'Sylhet', 'destination': 'Mymensingh', 'cost': 280.00, 'time': 160, 'distance': 180, 'rating': 4.4},
            {'source': 'Tangail', 'destination': 'Dhaka', 'cost': 190.00, 'time': 100, 'distance': 120, 'rating': 4.5},
            {'source': 'Kushtia', 'destination': 'Rajshahi', 'cost': 200.00, 'time': 120, 'distance': 130, 'rating': 4.3},
            {'source': 'Kushtia', 'destination': 'Khulna', 'cost': 230.00, 'time': 140, 'distance': 150, 'rating': 4.2},
            {'source': 'Bogra', 'destination': 'Dinajpur', 'cost': 180.00, 'time': 100, 'distance': 110, 'rating': 4.1},
            {'source': 'Dinajpur', 'destination': 'Rangpur', 'cost': 160.00, 'time': 90, 'distance': 100, 'rating': 4.3},
        ]
    
    def add_city(self, city_name):
        """Add city (simulated)"""
        return True, f"City '{city_name}' added (simulated)"
    
    def add_route(self, src_city, dst_city, route_cost, route_time, route_dist, route_rating):
        """Add route (simulated)"""
        return True, f"Route added successfully (simulated)"
    
    def close_db(self):
        print("Closing database connection (simulated)")
