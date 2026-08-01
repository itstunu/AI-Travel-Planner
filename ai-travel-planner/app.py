from flask import Flask, render_template, request, jsonify
from db import Database
from graph import Graph
from algorithms import SearchAlgorithms

app = Flask(__name__)
db = Database()
graph = Graph()
search_algo = None

def init_graph_data():
    global search_algo
    all_cities = db.get_cities()
    all_routes = db.get_routes()
    graph.build_graph(all_cities, all_routes)
    search_algo = SearchAlgorithms(graph)

init_graph_data()

@app.route('/')
def show_index():
    all_cities = db.get_cities()
    return render_template('index.html', cities=all_cities)

@app.route('/admin')
def show_admin():
    all_cities = db.get_cities()
    return render_template('admin.html', cities=all_cities)

@app.route('/api/cities', methods=['GET'])
def fetch_cities():
    all_cities = db.get_cities()
    return jsonify(all_cities)

@app.route('/api/routes', methods=['GET'])
def fetch_routes():
    all_routes = db.get_routes()
    return jsonify(all_routes)

@app.route('/api/add_city', methods=['POST'])
def insert_city():
    request_data = request.json
    city_name = request_data.get('name')
    
    if not city_name:
        return jsonify({'success': False, 'message': 'City name is required'})
    
    is_success, result_msg = db.add_city(city_name)
    
    if is_success:
        init_graph_data()
    
    return jsonify({'success': is_success, 'message': result_msg})

@app.route('/api/add_route', methods=['POST'])
def insert_route():
    request_data = request.json
    src_city = request_data.get('source')
    dst_city = request_data.get('destination')
    route_cost = request_data.get('cost')
    route_time = request_data.get('time')
    route_dist = request_data.get('distance')
    route_rating = request_data.get('rating', 0)
    
    if not all([src_city, dst_city, route_cost, route_time, route_dist]):
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    try:
        route_cost = float(route_cost)
        route_time = int(route_time)
        route_dist = float(route_dist)
        route_rating = float(route_rating)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid numeric values'})
    
    is_success, result_msg = db.add_route(src_city, dst_city, route_cost, route_time, route_dist, route_rating)
    
    if is_success:
        init_graph_data()
    
    return jsonify({'success': is_success, 'message': result_msg})

@app.route('/api/find_route', methods=['POST'])
def compute_route():
    request_data = request.json
    src_city = request_data.get('source')
    dst_city = request_data.get('destination')
    route_type = request_data.get('type')
    cost_budget = request_data.get('budget')
    time_limit = request_data.get('time')
    
    if cost_budget:
        try:
            cost_budget = float(cost_budget)
        except ValueError:
            cost_budget = None
    
    if time_limit:
        try:
            time_limit = int(time_limit)
        except ValueError:
            time_limit = None
    
    if not src_city or not dst_city:
        return jsonify({'success': False, 'message': 'Source and destination are required'})
    
    if route_type == 'cheapest':
        result_path, total_cost, total_time, avg_rating = search_algo.uniform_cost_search(src_city, dst_city, cost_budget, time_limit)
    elif route_type == 'fastest':
        result_path, total_cost, total_time, avg_rating = search_algo.greedy_best_first_search(src_city, dst_city, cost_budget, time_limit)
    elif route_type == 'best':
        result_path, total_cost, total_time, avg_rating = search_algo.a_star_search(src_city, dst_city, cost_budget, time_limit)
    elif route_type == 'least_stops':
        result_path, total_cost, total_time, avg_rating = search_algo.bfs(src_city, dst_city, cost_budget, time_limit)
    else:
        return jsonify({'success': False, 'message': 'Invalid route type'})
    
    if not result_path:
        return jsonify({
            'success': False,
            'message': 'No route found matching your criteria. Try adjusting budget or time constraints.'
        })
    
    return jsonify({
        'success': True,
        'path': result_path,
        'total_cost': round(total_cost, 2),
        'total_time': total_time,
        'avg_rating': round(avg_rating, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)