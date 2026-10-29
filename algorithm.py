"""
algorithm.py - DAA Implementation: Dijkstra's Shortest Path Algorithm
Flight Route Planner Project

This module defines:
1. The predefined weighted undirected graph of 9 Indian airports.
2. Dijkstra's shortest-path algorithm using Python's standard `heapq` module.
3. Route reconstruction and validation helpers.

DISCLAIMER:
All distances are illustrative demonstration values in kilometres (km)
prepared for academic study and DAA viva demonstrations. They are not
verified flight nautical miles or live commercial airline schedules.
"""

import heapq
from typing import Dict, List, Optional, Any


# -------------------------------------------------------------------------
# 1. Airport Graph Representation (Adjacency List as Dictionary of Dictionaries)
# -------------------------------------------------------------------------
# Vertices (9 Airports):
# 1. Delhi (DEL)
# 2. Jaipur (JAI)
# 3. Lucknow (LKO)
# 4. Ahmedabad (AMD)
# 5. Mumbai (BOM)
# 6. Hyderabad (HYD)
# 7. Bengaluru (BLR)
# 8. Chennai (MAA)
# 9. Kolkata (CCU)
#
# All edge weights are non-negative illustrative flight distances in kilometres (km).
# The graph is undirected (symmetric: weight(u, v) == weight(v, u)).
# -------------------------------------------------------------------------

AIRPORT_GRAPH: Dict[str, Dict[str, int]] = {
    "Delhi": {
        "Jaipur": 280,
        "Lucknow": 420,
        "Kolkata": 1300,
    },
    "Jaipur": {
        "Delhi": 280,
        "Mumbai": 1145,
        "Ahmedabad": 720,
    },
    "Lucknow": {
        "Delhi": 420,
        "Kolkata": 890,
        "Hyderabad": 1080,
    },
    "Ahmedabad": {
        "Jaipur": 720,
        "Mumbai": 440,
    },
    "Mumbai": {
        "Jaipur": 1145,
        "Ahmedabad": 440,
        "Bengaluru": 570,
        "Hyderabad": 620,
    },
    "Hyderabad": {
        "Lucknow": 1080,
        "Mumbai": 620,
        "Bengaluru": 500,
        "Chennai": 520,
        "Kolkata": 1180,
    },
    "Bengaluru": {
        "Mumbai": 570,
        "Hyderabad": 500,
        "Chennai": 290,
    },
    "Chennai": {
        "Bengaluru": 290,
        "Hyderabad": 520,
        "Kolkata": 1360,
    },
    "Kolkata": {
        "Delhi": 1300,
        "Lucknow": 890,
        "Hyderabad": 1180,
        "Chennai": 1360,
    },
}

# Airport Metadata for rich UI presentation (IATA code, full city name, region)
AIRPORT_INFO: Dict[str, Dict[str, str]] = {
    "Delhi": {
        "code": "DEL",
        "city": "New Delhi",
        "airport_name": "Indira Gandhi International Airport",
        "state": "Delhi NCR",
    },
    "Jaipur": {
        "code": "JAI",
        "city": "Jaipur",
        "airport_name": "Jaipur International Airport",
        "state": "Rajasthan",
    },
    "Lucknow": {
        "code": "LKO",
        "city": "Lucknow",
        "airport_name": "Chaudhary Charan Singh International Airport",
        "state": "Uttar Pradesh",
    },
    "Ahmedabad": {
        "code": "AMD",
        "city": "Ahmedabad",
        "airport_name": "Sardar Vallabhbhai Patel International Airport",
        "state": "Gujarat",
    },
    "Mumbai": {
        "code": "BOM",
        "city": "Mumbai",
        "airport_name": "Chhatrapati Shivaji Maharaj International Airport",
        "state": "Maharashtra",
    },
    "Hyderabad": {
        "code": "HYD",
        "city": "Hyderabad",
        "airport_name": "Rajiv Gandhi International Airport",
        "state": "Telangana",
    },
    "Bengaluru": {
        "code": "BLR",
        "city": "Bengaluru",
        "airport_name": "Kempegowda International Airport",
        "state": "Karnataka",
    },
    "Chennai": {
        "code": "MAA",
        "city": "Chennai",
        "airport_name": "Chennai International Airport",
        "state": "Tamil Nadu",
    },
    "Kolkata": {
        "code": "CCU",
        "city": "Kolkata",
        "airport_name": "Netaji Subhash Chandra Bose International Airport",
        "state": "West Bengal",
    },
}


def get_all_airports(graph: Optional[Dict[str, Dict[str, int]]] = None) -> List[str]:
    """Return a sorted list of all airport names present in the graph."""
    if graph is None:
        graph = AIRPORT_GRAPH
    return sorted(list(graph.keys()))


def find_shortest_route(
    source: str,
    destination: str,
    graph: Optional[Dict[str, Dict[str, int]]] = None,
) -> Dict[str, Any]:
    """
    Find the shortest route between two airports using Dijkstra's Algorithm.

    Parameters:
        source (str): The starting airport name.
        destination (str): The target destination airport name.
        graph (dict, optional): The graph adjacency list. Defaults to AIRPORT_GRAPH.

    Returns:
        dict: A structured response containing:
            - success (bool): True if route found, False otherwise.
            - error (str, optional): Error message if success is False.
            - source (str): Starting airport.
            - destination (str): Target airport.
            - route (list): List of airport names visited from source to destination.
            - total_distance (int or float): Total path weight in km.
            - num_airports (int): Number of airports in the path.
            - num_legs (int): Number of flight legs (num_airports - 1).
            - legs_detail (list): Individual leg breakdowns with distance.
            - algorithm (str): "Dijkstra's Algorithm".

    Complexity:
        Time Complexity:  O((V + E) log V) with binary min-heap (heapq)
        Space Complexity: O(V + E) for adjacency list, distances, and priority queue
    """
    if graph is None:
        graph = AIRPORT_GRAPH

    # 1. Input Validation: Check if source and destination exist in graph
    if not source or not destination:
        return {
            "success": False,
            "error": "Both source and destination airports must be specified.",
        }

    if source not in graph:
        return {
            "success": False,
            "error": f"Source airport '{source}' does not exist in the airport graph.",
        }

    if destination not in graph:
        return {
            "success": False,
            "error": f"Destination airport '{destination}' does not exist in the airport graph.",
        }

    # 2. Case: Identical Source and Destination
    if source == destination:
        return {
            "success": True,
            "source": source,
            "destination": destination,
            "route": [source],
            "total_distance": 0,
            "num_airports": 1,
            "num_legs": 0,
            "legs_detail": [],
            "algorithm": "Dijkstra's Algorithm",
            "message": "Source and destination are identical. Distance is 0 km.",
        }

    # 3. Initialization of Dijkstra's Data Structures
    # distances: maps each airport to the currently known shortest distance from source
    # Initialize all distances to infinity, except source which is 0
    distances: Dict[str, float] = {airport: float("inf") for airport in graph}
    distances[source] = 0

    # previous: maps each airport to its immediate predecessor on the shortest path
    previous: Dict[str, Optional[str]] = {airport: None for airport in graph}

    # priority_queue: min-heap storing tuples of (current_shortest_distance, airport_name)
    # Binary min-heap guarantees we always extract the unvisited vertex with smallest tentative distance
    priority_queue: List[tuple] = [(0, source)]

    # 4. Main Dijkstra Relaxation Loop
    while priority_queue:
        current_distance, current_airport = heapq.heappop(priority_queue)

        # Lazy deletion check:
        # If we popped an outdated longer distance entry, ignore it
        if current_distance > distances[current_airport]:
            continue

        # Early termination:
        # If we have extracted the destination from the priority queue,
        # its shortest distance is guaranteed to be optimal (non-negative edge weights).
        if current_airport == destination:
            break

        # Edge relaxation step for all neighbors of current_airport:
        for neighbor, weight in graph[current_airport].items():
            # Edge weight validation (DAA requirement: non-negative weights)
            if weight < 0:
                return {
                    "success": False,
                    "error": "Negative edge weight detected. Dijkstra's algorithm requires non-negative weights.",
                }

            distance_through_current = current_distance + weight

            # Relaxation condition:
            # If path through current_airport to neighbor is strictly shorter
            if distance_through_current < distances[neighbor]:
                distances[neighbor] = distance_through_current
                previous[neighbor] = current_airport
                heapq.heappush(priority_queue, (distance_through_current, neighbor))

    # 5. Check if Destination is Reachable
    if distances[destination] == float("inf"):
        return {
            "success": False,
            "error": f"No connected flight route exists between '{source}' and '{destination}'.",
        }

    # 6. Shortest Path Reconstruction (Backtracking from destination to source)
    route: List[str] = []
    curr: Optional[str] = destination
    while curr is not None:
        route.append(curr)
        curr = previous[curr]
    route.reverse()

    # 7. Build Detailed Flight Legs Breakdown
    legs_detail: List[Dict[str, Any]] = []
    for i in range(len(route) - 1):
        origin = route[i]
        dest = route[i + 1]
        leg_distance = graph[origin][dest]
        legs_detail.append({
            "leg_number": i + 1,
            "from_airport": origin,
            "to_airport": dest,
            "from_code": AIRPORT_INFO.get(origin, {}).get("code", "---"),
            "to_code": AIRPORT_INFO.get(dest, {}).get("code", "---"),
            "distance_km": leg_distance,
        })

    total_dist = int(distances[destination]) if distances[destination].is_integer() else distances[destination]

    return {
        "success": True,
        "source": source,
        "destination": destination,
        "route": route,
        "total_distance": total_dist,
        "num_airports": len(route),
        "num_legs": len(route) - 1,
        "legs_detail": legs_detail,
        "algorithm": "Dijkstra's Algorithm",
        "message": f"Optimal route calculated with {len(route) - 1} flight leg(s).",
    }
