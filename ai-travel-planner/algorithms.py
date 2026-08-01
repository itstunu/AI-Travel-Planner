from collections import deque
import heapq

class SearchAlgorithms:
    def __init__(self, graph):
        self.graph = graph
    
    def bfs(self, start, goal, budget=None, max_time=None):
        """Breadth-First Search - Find path with least stops"""
        if start == goal:
            return [start], 0, 0, 0
        
        queue = deque([(start, [start], 0, 0)])  # (city, path, cost, time)
        visited = set([start])
        best_path = None
        best_cost = 0
        best_time = float('inf')
        
        while queue:
            current, path, total_cost, total_time = queue.popleft()
            
            for neighbor in self.graph.get_neighbors(current):
                route = self.graph.get_route_info(current, neighbor)
                
                if not route:
                    continue
                
                # Apply filters
                if budget and total_cost + route['cost'] > budget:
                    continue
                if max_time and total_time + route['time'] > max_time:
                    continue
                
                new_cost = total_cost + route['cost']
                new_time = total_time + route['time']
                
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    
                    if neighbor == goal:
                        # BFS returns first found (least stops)
                        return new_path, new_cost, new_time, self.calculate_avg_rating(new_path)
                    
                    visited.add(neighbor)
                    queue.append((neighbor, new_path, new_cost, new_time))
        
        return None, 0, 0, 0
    
    def uniform_cost_search(self, start, goal, budget=None, max_time=None):
        """Uniform Cost Search - Find cheapest route based on total cost"""
        if start == goal:
            return [start], 0, 0, 0
        
        # Priority queue: (total_cost, total_time, city, path)
        pq = [(0, 0, start, [start])]
        visited = {}
        
        while pq:
            total_cost, total_time, current, path = heapq.heappop(pq)
            
            # Skip if we've found a cheaper path to this city
            if current in visited and visited[current] <= total_cost:
                continue
            
            visited[current] = total_cost
            
            if current == goal:
                return path, total_cost, total_time, self.calculate_avg_rating(path)
            
            for neighbor in self.graph.get_neighbors(current):
                route = self.graph.get_route_info(current, neighbor)
                
                if not route:
                    continue
                
                new_cost = total_cost + route['cost']
                new_time = total_time + route['time']
                
                # Apply filters
                if budget and new_cost > budget:
                    continue
                if max_time and new_time > max_time:
                    continue
                
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_cost, new_time, neighbor, new_path))
        
        return None, 0, 0, 0
    
    def greedy_best_first_search(self, start, goal, budget=None, max_time=None):
        """Greedy Best-First Search - Find fastest route based on TOTAL accumulated time"""
        if start == goal:
            return [start], 0, 0, 0
        
        # Priority queue: (total_time, total_cost, city, path)
        # This prioritizes TOTAL time, not just the last edge time
        pq = [(0, 0, start, [start])]
        visited = {}
        
        while pq:
            total_time, total_cost, current, path = heapq.heappop(pq)
            
            # Skip if we've found a faster path to this city
            if current in visited and visited[current] <= total_time:
                continue
            
            visited[current] = total_time
            
            if current == goal:
                return path, total_cost, total_time, self.calculate_avg_rating(path)
            
            for neighbor in self.graph.get_neighbors(current):
                route = self.graph.get_route_info(current, neighbor)
                
                if not route:
                    continue
                
                new_time = total_time + route['time']
                new_cost = total_cost + route['cost']
                
                # Apply filters
                if budget and new_cost > budget:
                    continue
                if max_time and new_time > max_time:
                    continue
                
                new_path = path + [neighbor]
                # Priority based on TOTAL accumulated time (not just edge time)
                heapq.heappush(pq, (new_time, new_cost, neighbor, new_path))
        
        return None, 0, 0, 0
    
    def a_star_search(self, start, goal, budget=None, max_time=None):
        """A* Algorithm - Find best route using f(n) = cost + heuristic(distance)"""
        if start == goal:
            return [start], 0, 0, 0
        
        def heuristic(city1, city2):
            # Get direct route distance as heuristic
            direct_route = self.graph.get_route_info(city1, city2)
            if direct_route:
                return direct_route['distance'] * 0.5  # Use distance-based heuristic
            # If no direct route, estimate based on average
            return 100
        
        # Priority queue: (f_score, total_cost, total_time, city, path)
        pq = [(0, 0, 0, start, [start])]
        visited = {}
        g_score = {start: 0}
        
        while pq:
            f_score, total_cost, total_time, current, path = heapq.heappop(pq)
            
            if current in visited and visited[current] <= g_score.get(current, float('inf')):
                continue
            
            visited[current] = g_score.get(current, float('inf'))
            
            if current == goal:
                return path, total_cost, total_time, self.calculate_avg_rating(path)
            
            for neighbor in self.graph.get_neighbors(current):
                route = self.graph.get_route_info(current, neighbor)
                
                if not route:
                    continue
                
                new_cost = total_cost + route['cost']
                new_time = total_time + route['time']
                
                # Apply filters
                if budget and new_cost > budget:
                    continue
                if max_time and new_time > max_time:
                    continue
                
                tentative_g = g_score[current] + route['cost']
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    new_path = path + [neighbor]
                    
                    # f(n) = g(n) + h(n)
                    h = heuristic(neighbor, goal)
                    f = tentative_g + h
                    
                    heapq.heappush(pq, (f, new_cost, new_time, neighbor, new_path))
        
        return None, 0, 0, 0
    
    def calculate_avg_rating(self, path):
        """Calculate average rating for a path"""
        if len(path) < 2:
            return 0
        
        total_rating = 0
        count = 0
        
        for i in range(len(path) - 1):
            route = self.graph.get_route_info(path[i], path[i+1])
            if route:
                total_rating += route['rating']
                count += 1
        
        return total_rating / count if count > 0 else 0