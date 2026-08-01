class Graph:
    def __init__(self):
        self.adj_list = {}
        self.route_data = {}
    
    def build_graph(self, city_list, route_list):
        for each_city in city_list:
            self.adj_list[each_city['name']] = []
        
        for each_route in route_list:
            source_city = each_route['source']
            dest_city = each_route['destination']
            
            self.adj_list[source_city].append(dest_city)
            
            route_key = f"{source_city}->{dest_city}"
            self.route_data[route_key] = {
                'cost': float(each_route['cost']),
                'time': each_route['time'],
                'distance': float(each_route['distance']),
                'rating': float(each_route['rating']) if each_route['rating'] else 0.0
            }
    
    def get_neighbors(self, city_name):
        return self.adj_list.get(city_name, [])
    
    def get_route_info(self, source_city, dest_city):
        route_key = f"{source_city}->{dest_city}"
        return self.route_data.get(route_key)