"""
test_algorithm.py - Unit Test Suite for Dijkstra's Flight Route Planner
For MCA DAA Practical Examination & Evaluation

Tests cover:
1. Delhi to Bengaluru returns the required 1,995 km route.
2. Ahmedabad to Mumbai returns 440 km direct route.
3. Same source and destination returns distance zero.
4. Reverse-direction routes work identically for undirected graph.
5. Invalid airport names are handled correctly.
6. A valid route can be properly reconstructed with valid edges.
7. Unreachable destinations are handled gracefully in disconnected graphs.
"""

import unittest
from algorithm import (
    find_shortest_route,
    AIRPORT_GRAPH,
    get_all_airports,
    AIRPORT_INFO,
)


class TestFlightRoutePlanner(unittest.TestCase):

    def setUp(self):
        """Set up standard graph and test instances before each test."""
        self.graph = AIRPORT_GRAPH

    # Test 1: Required route Delhi -> Bengaluru
    def test_delhi_to_bengaluru_route(self):
        """Verify Delhi -> Bengaluru produces 1,995 km across 3 flight legs."""
        result = find_shortest_route("Delhi", "Bengaluru", self.graph)

        self.assertTrue(result["success"], "Dijkstra search should succeed.")
        self.assertEqual(result["total_distance"], 1995, "Total distance must be exactly 1,995 km.")
        self.assertEqual(
            result["route"],
            ["Delhi", "Jaipur", "Mumbai", "Bengaluru"],
            "Route must be Delhi -> Jaipur -> Mumbai -> Bengaluru.",
        )
        self.assertEqual(result["num_airports"], 4, "Should visit 4 airports.")
        self.assertEqual(result["num_legs"], 3, "Should have 3 flight legs.")
        self.assertEqual(result["algorithm"], "Dijkstra's Algorithm")

    # Test 2: Required route Ahmedabad -> Mumbai
    def test_ahmedabad_to_mumbai_direct_route(self):
        """Verify Ahmedabad -> Mumbai returns direct route of 440 km across 1 flight leg."""
        result = find_shortest_route("Ahmedabad", "Mumbai", self.graph)

        self.assertTrue(result["success"], "Dijkstra search should succeed.")
        self.assertEqual(result["total_distance"], 440, "Total distance must be exactly 440 km.")
        self.assertEqual(
            result["route"],
            ["Ahmedabad", "Mumbai"],
            "Route must be direct Ahmedabad -> Mumbai.",
        )
        self.assertEqual(result["num_airports"], 2)
        self.assertEqual(result["num_legs"], 1)

    # Test 3: Same source and destination
    def test_same_source_and_destination(self):
        """Verify same source and destination returns 0 km distance and 0 legs."""
        airports_to_test = ["Delhi", "Mumbai", "Bengaluru"]
        for ap in airports_to_test:
            with self.subTest(airport=ap):
                result = find_shortest_route(ap, ap, self.graph)
                self.assertTrue(result["success"])
                self.assertEqual(result["total_distance"], 0)
                self.assertEqual(result["route"], [ap])
                self.assertEqual(result["num_airports"], 1)
                self.assertEqual(result["num_legs"], 0)
                self.assertEqual(len(result["legs_detail"]), 0)

    # Test 4: Reverse-direction routes (undirected graph property)
    def test_reverse_direction_routes(self):
        """Verify undirected graph symmetry: route(A, B) distance == route(B, A) distance."""
        # 1. Bengaluru -> Delhi
        result_rev1 = find_shortest_route("Bengaluru", "Delhi", self.graph)
        self.assertTrue(result_rev1["success"])
        self.assertEqual(result_rev1["total_distance"], 1995)
        self.assertEqual(
            result_rev1["route"],
            ["Bengaluru", "Mumbai", "Jaipur", "Delhi"],
        )

        # 2. Mumbai -> Ahmedabad
        result_rev2 = find_shortest_route("Mumbai", "Ahmedabad", self.graph)
        self.assertTrue(result_rev2["success"])
        self.assertEqual(result_rev2["total_distance"], 440)
        self.assertEqual(result_rev2["route"], ["Mumbai", "Ahmedabad"])

    # Test 5: Invalid airport names
    def test_invalid_airport_handling(self):
        """Verify invalid or non-existent airport names are handled gracefully."""
        # Invalid source
        res1 = find_shortest_route("Atlantis", "Delhi", self.graph)
        self.assertFalse(res1["success"])
        self.assertIn("error", res1)
        self.assertIn("Atlantis", res1["error"])

        # Invalid destination
        res2 = find_shortest_route("Delhi", "Gotham", self.graph)
        self.assertFalse(res2["success"])
        self.assertIn("error", res2)
        self.assertIn("Gotham", res2["error"])

        # Empty string
        res3 = find_shortest_route("", "Delhi", self.graph)
        self.assertFalse(res3["success"])
        self.assertIn("error", res3)

    # Test 6: Route reconstruction validity
    def test_route_reconstruction_integrity(self):
        """Verify that every step in a calculated route is a valid connected edge."""
        test_pairs = [
            ("Delhi", "Chennai"),
            ("Kolkata", "Ahmedabad"),
            ("Jaipur", "Hyderabad"),
            ("Lucknow", "Bengaluru"),
        ]

        for src, dst in test_pairs:
            with self.subTest(pair=f"{src}->{dst}"):
                res = find_shortest_route(src, dst, self.graph)
                self.assertTrue(res["success"])
                route = res["route"]

                # Ensure start and end match
                self.assertEqual(route[0], src)
                self.assertEqual(route[-1], dst)

                # Ensure all consecutive edges exist in graph and sum matches
                calculated_sum = 0
                for i in range(len(route) - 1):
                    u = route[i]
                    v = route[i + 1]
                    self.assertIn(v, self.graph[u], f"Edge ({u}, {v}) must exist in graph.")
                    calculated_sum += self.graph[u][v]

                self.assertEqual(calculated_sum, res["total_distance"])

    # Test 7: Unreachable destination handling
    def test_unreachable_destination_in_disconnected_graph(self):
        """Verify disconnected components are handled cleanly with appropriate error message."""
        disconnected_graph = {
            "Delhi": {"Jaipur": 280},
            "Jaipur": {"Delhi": 280},
            "PortBlair": {"Havelock": 60},  # Isolated island component
            "Havelock": {"PortBlair": 60},
        }

        res = find_shortest_route("Delhi", "PortBlair", disconnected_graph)
        self.assertFalse(res["success"])
        self.assertIn("error", res)
        self.assertIn("No connected flight route exists", res["error"])

    # Additional Graph Metadata and Integrity Tests
    def test_graph_properties(self):
        """Verify graph has exactly 9 airports and is fully symmetric."""
        airports = get_all_airports(self.graph)
        self.assertEqual(len(airports), 9)
        expected_airports = [
            "Ahmedabad", "Bengaluru", "Chennai", "Delhi",
            "Hyderabad", "Jaipur", "Kolkata", "Lucknow", "Mumbai"
        ]
        self.assertEqual(airports, expected_airports)

        # Symmetry test
        for u in self.graph:
            for v, weight in self.graph[u].items():
                self.assertIn(v, self.graph, f"Neighbor {v} must be a known vertex.")
                self.assertIn(u, self.graph[v], f"Reverse edge ({v}, {u}) must exist.")
                self.assertEqual(
                    self.graph[u][v],
                    self.graph[v][u],
                    f"Edge weights for ({u}, {v}) and ({v}, {u}) must be equal.",
                )
                self.assertGreater(weight, 0, "Distance must be strictly positive.")


if __name__ == "__main__":
    unittest.main()
