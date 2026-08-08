import mysql.connector
from mysql.connector import Error
import os
import streamlit as st

class Database:
    def __init__(self):
        self.db_connection = None
        self.connect_db()
    
    def connect_db(self):
        try:
            # Try to get database credentials from environment variables (Streamlit Cloud secrets)
            # or fallback to local development values
            
            # For Streamlit Cloud, use secrets
            if hasattr(st, 'secrets') and 'mysql' in st.secrets:
                db_config = {
                    'host': st.secrets.mysql.host,
                    'user': st.secrets.mysql.user,
                    'password': st.secrets.mysql.password,
                    'database': st.secrets.mysql.database,
                    'port': st.secrets.mysql.get('port', 3306)
                }
            else:
                # Local development
                db_config = {
                    'host': os.getenv('DB_HOST', 'localhost'),
                    'user': os.getenv('DB_USER', 'root'),
                    'password': os.getenv('DB_PASSWORD', ''),
                    'database': os.getenv('DB_NAME', 'travel_ai')
                }
            
            self.db_connection = mysql.connector.connect(**db_config)
            
            if self.db_connection.is_connected():
                print(f"Connected to MySQL database at {db_config['host']}")
                
        except Error as db_error:
            print(f"Error connecting to MySQL: {db_error}")
            # Re-raise to handle in the calling code
            raise
    
    def get_cities(self):
        try:
            db_cursor = self.db_connection.cursor(dictionary=True)
            db_cursor.execute("SELECT * FROM cities ORDER BY name")
            city_list = db_cursor.fetchall()
            db_cursor.close()
            return city_list
        except Error as db_error:
            print(f"Error fetching cities: {db_error}")
            return []
    
    def get_routes(self):
        try:
            db_cursor = self.db_connection.cursor(dictionary=True)
            db_cursor.execute("SELECT * FROM routes ORDER BY source, destination")
            route_list = db_cursor.fetchall()
            db_cursor.close()
            return route_list
        except Error as db_error:
            print(f"Error fetching routes: {db_error}")
            return []
    
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
