"""
app.py - Flask Web Application for Flight Route Planner
DAA Mini Project: Shortest Path Finding Using Dijkstra's Algorithm

This module provides:
1. Route '/' (GET): Renders the main dashboard with airport selectors.
2. Route '/' (POST): Handles standard HTML form submission and renders results.
3. Route '/api/route' (POST): REST API endpoint returning JSON for dynamic UI updates.
4. Route '/api/graph' (GET): Returns the airport network data for visual display.
"""

from flask import Flask, render_template, request, jsonify
from algorithm import (
    AIRPORT_GRAPH,
    AIRPORT_INFO,
    find_shortest_route,
    get_all_airports,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page route.
    Handles both GET requests (displaying the form) and
    POST requests (calculating route and returning template with results).
    """
    airports = get_all_airports()
    result = None
    error = None
    selected_source = ""
    selected_destination = ""

    if request.method == "POST":
        selected_source = request.form.get("source", "").strip()
        selected_destination = request.form.get("destination", "").strip()

        if not selected_source or not selected_destination:
            error = "Please select both a departure airport and an arrival airport."
        else:
            route_result = find_shortest_route(selected_source, selected_destination)
            if route_result["success"]:
                result = route_result
            else:
                error = route_result.get("error", "An error occurred while finding the route.")

    return render_template(
        "index.html",
        airports=airports,
        airport_info=AIRPORT_INFO,
        graph=AIRPORT_GRAPH,
        result=result,
        error=error,
        selected_source=selected_source,
        selected_destination=selected_destination,
    )


@app.route("/api/route", methods=["POST"])
def api_route():
    """
    JSON API endpoint for asynchronous (AJAX/Fetch) route calculation.
    Enables instant results without full-page reloads.
    """
    data = request.get_json(silent=True) or request.form
    source = data.get("source", "").strip()
    destination = data.get("destination", "").strip()

    if not source or not destination:
        return jsonify({
            "success": False,
            "error": "Both departure and arrival airports are required.",
        }), 400

    route_result = find_shortest_route(source, destination)
    status_code = 200 if route_result["success"] else 400
    return jsonify(route_result), status_code


@app.route("/api/graph", methods=["GET"])
def api_graph():
    """
    JSON endpoint providing the network graph structure and airport metadata.
    Used for front-end rendering and educational inspection.
    """
    return jsonify({
        "graph": AIRPORT_GRAPH,
        "airports": AIRPORT_INFO,
    })


if __name__ == "__main__":
    # Run development server locally on port 5000
    print("=" * 60)
    print(" Flight Route Planner - DAA Mini Project")
    print(" Algorithm: Dijkstra's Shortest Path Algorithm (heapq)")
    print(" Running locally at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=True)
