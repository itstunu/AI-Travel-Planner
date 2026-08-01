import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.db_connection = None
        self.connect_db()
    
    def connect_db(self):
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='travel_ai'
            )
            if self.db_connection.is_connected():
                print("Connected to MySQL database")
        except Error as db_error:
            print(f"Error connecting to MySQL: {db_error}")
    
    def get_cities(self):
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute("SELECT * FROM cities ORDER BY name")
        city_list = db_cursor.fetchall()
        db_cursor.close()
        return city_list
    
    def get_routes(self):
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute("SELECT * FROM routes")
        route_list = db_cursor.fetchall()
        db_cursor.close()
        return route_list
    
    def add_city(self, city_name):
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute("INSERT INTO cities (name) VALUES (%s)", (city_name,))
            self.db_connection.commit()
            db_cursor.close()
            return True, "City added successfully"
        except Error as db_error:
            return False, f"Error: {db_error}"
    
    def add_route(self, src_city, dst_city, route_cost, route_time, route_dist, route_rating):
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute("""
                INSERT INTO routes (source, destination, cost, time, distance, rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (src_city, dst_city, route_cost, route_time, route_dist, route_rating))
            self.db_connection.commit()
            db_cursor.close()
            return True, "Route added successfully"
        except Error as db_error:
            return False, f"Error: {db_error}"
    
    def close_db(self):
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            print("Database connection closed")