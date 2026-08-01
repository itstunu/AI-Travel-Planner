// Global variables
let cities = [];
let routes = [];

// Load data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadRoutes();
    
    // Setup form handlers
    const addCityForm = document.getElementById('addCityForm');
    if (addCityForm) {
        addCityForm.addEventListener('submit', handleAddCity);
    }
    
    const addRouteForm = document.getElementById('addRouteForm');
    if (addRouteForm) {
        addRouteForm.addEventListener('submit', handleAddRoute);
    }
});

// Load all routes
async function loadRoutes() {
    try {
        const response = await fetch('/api/routes');
        routes = await response.json();
        displayRoutes();
    } catch (error) {
        console.error('Error loading routes:', error);
    }
}

// Display routes in table
function displayRoutes() {
    const tbody = document.getElementById('routesTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    routes.forEach(route => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${route.source}</td>
            <td>${route.destination}</td>
            <td>৳${parseFloat(route.cost).toFixed(2)}</td>
            <td>${route.time} min</td>
            <td>${parseFloat(route.distance).toFixed(1)} km</td>
            <td>
                <span class="badge bg-warning text-dark">
                    ${parseFloat(route.rating).toFixed(1)} ⭐
                </span>
            </td>
        `;
    });
}

// Find route based on selected type
async function findRoute(type) {
    const source = document.getElementById('source').value;
    const destination = document.getElementById('destination').value;
    const budget = document.getElementById('budget').value;
    const maxTime = document.getElementById('maxTime').value;
    
    // Validate inputs
    if (!source || !destination) {
        showError('Please select both source and destination cities');
        return;
    }
    
    if (source === destination) {
        showError('Source and destination cannot be the same');
        return;
    }
    
    // Hide previous results
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch('/api/find_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source: source,
                destination: destination,
                type: type,
                budget: budget || null,
                time: maxTime || null
            })
        });
        
        const data = await response.json();
        
        // Hide loading
        hideLoading();
        
        if (data.success) {
            displayResult(data);
        } else {
            showError(data.message);
        }
    } catch (error) {
        hideLoading();
        showError('An error occurred while finding the route. Please try again.');
        console.error('Error:', error);
    }
}

// Display route result
function displayResult(data) {
    document.getElementById('resultPath').textContent = data.path.join(' → ');
    document.getElementById('resultCost').textContent = `৳${data.total_cost.toFixed(2)}`;
    document.getElementById('resultTime').textContent = `${data.total_time} minutes`;
    document.getElementById('resultRating').textContent = `${data.avg_rating.toFixed(1)} ⭐`;
    
    document.getElementById('result').style.display = 'block';
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    
    if (errorDiv && errorMessage) {
        errorMessage.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

// Show success message (for admin panel)
function showSuccess(message) {
    const msgDiv = document.getElementById('adminMessage');
    if (msgDiv) {
        msgDiv.className = 'alert alert-success';
        msgDiv.textContent = message;
        msgDiv.style.display = 'block';
        
        setTimeout(() => {
            msgDiv.style.display = 'none';
        }, 3000);
    }
}

// Show loading state
function showLoading() {
    const buttons = document.querySelectorAll('.btn-group .btn');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.dataset.originalText = btn.textContent;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Searching...';
    });
}

// Hide loading state
function hideLoading() {
    const buttons = document.querySelectorAll('.btn-group .btn');
    buttons.forEach(btn => {
        btn.disabled = false;
        btn.textContent = btn.dataset.originalText;
    });
}

// Handle add city form submission
async function handleAddCity(event) {
    event.preventDefault();
    
    const cityName = document.getElementById('cityName').value.trim();
    
    if (!cityName) {
        showError('Please enter a city name');
        return;
    }
    
    try {
        const response = await fetch('/api/add_city', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: cityName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            document.getElementById('cityName').value = '';
            
            // Reload page after 1 second to refresh city lists
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Error adding city');
        console.error('Error:', error);
    }
}

// Handle add route form submission
async function handleAddRoute(event) {
    event.preventDefault();
    
    const source = document.getElementById('routeSource').value;
    const destination = document.getElementById('routeDestination').value;
    const cost = document.getElementById('routeCost').value;
    const time = document.getElementById('routeTime').value;
    const distance = document.getElementById('routeDistance').value;
    const rating = document.getElementById('routeRating').value || 4.0;
    
    if (source === destination) {
        showError('Source and destination cannot be the same');
        return;
    }
    
    try {
        const response = await fetch('/api/add_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source: source,
                destination: destination,
                cost: parseFloat(cost),
                time: parseInt(time),
                distance: parseFloat(distance),
                rating: parseFloat(rating)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            document.getElementById('addRouteForm').reset();
            
            // Reload routes on main page
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Error adding route');
        console.error('Error:', error);
    }
}