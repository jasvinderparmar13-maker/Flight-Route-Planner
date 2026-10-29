# Flight Route Planner Using Python Programming

An academic web application developed for **MCA-level Design and Analysis of Algorithms (DAA)** practical evaluation. The application finds the optimal (shortest-distance) flight itinerary between major Indian airports using **Dijkstra’s Shortest-Path Algorithm** implemented with Python's standard `heapq` priority queue.

---

## 1. Project Objective

- Model an Indian domestic flight network as a **weighted, undirected graph**.
- Implement **Dijkstra's Shortest Path Algorithm** from scratch using Python without third-party graph or shortest-path libraries (such as NetworkX).
- Utilize a **binary min-heap (`heapq`)** for efficient vertex extraction ($O(\log V)$).
- Provide a responsive, airline-inspired web interface built using **Flask, HTML5, CSS3, and JavaScript**.
- Ensure reliable handling of edge cases (identical origin/destination, reverse paths, disconnected nodes, invalid inputs).

---

## 2. Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3 | Core algorithmic logic & backend |
| **Web Framework** | Flask | Lightweight WSGI web application routing |
| **Data Structures** | Python `heapq`, `dict` | Min-heap priority queue & adjacency list |
| **Frontend Markup** | HTML5 (Jinja2) | Semantic, accessible web structure |
| **Frontend Styling** | CSS3 (Custom Airline Theme) | Modern navy-and-white responsive UI |
| **Frontend Scripting**| Vanilla JavaScript | Dynamic AJAX requests & interactive UI swap |
| **Unit Testing** | Python `unittest` | Automated verification of test cases |
| **IDE** | Visual Studio Code | Development & debugging environment |

> **Note:** React, Node.js, external databases, or paid APIs are deliberately avoided to maintain simplicity, academic clarity, and ease of explanation during viva voce.

---

## 3. Airport Graph Representation

The network consists of **9 vertices (airports)** and **15 undirected weighted edges** stored in Python as an adjacency list using a **dictionary of dictionaries** (`dict[str, dict[str, int]]`):

### Vertices (Airports)
1. **Delhi (DEL)** - Indira Gandhi International Airport
2. **Jaipur (JAI)** - Jaipur International Airport
3. **Lucknow (LKO)** - Chaudhary Charan Singh International Airport
4. **Ahmedabad (AMD)** - Sardar Vallabhbhai Patel International Airport
5. **Mumbai (BOM)** - Chhatrapati Shivaji Maharaj International Airport
6. **Hyderabad (HYD)** - Rajiv Gandhi International Airport
7. **Bengaluru (BLR)** - Kempegowda International Airport
8. **Chennai (MAA)** - Chennai International Airport
9. **Kolkata (CCU)** - Netaji Subhash Chandra Bose International Airport

### Graph Adjacency List Structure
```python
AIRPORT_GRAPH = {
    "Delhi":     {"Jaipur": 280, "Lucknow": 420, "Kolkata": 1300},
    "Jaipur":    {"Delhi": 280, "Mumbai": 1145, "Ahmedabad": 720},
    "Lucknow":   {"Delhi": 420, "Kolkata": 890, "Hyderabad": 1080},
    "Ahmedabad": {"Jaipur": 720, "Mumbai": 440},
    "Mumbai":    {"Jaipur": 1145, "Ahmedabad": 440, "Bengaluru": 570, "Hyderabad": 620},
    "Hyderabad": {"Lucknow": 1080, "Mumbai": 620, "Bengaluru": 500, "Chennai": 520, "Kolkata": 1180},
    "Bengaluru": {"Mumbai": 570, "Hyderabad": 500, "Chennai": 290},
    "Chennai":   {"Bengaluru": 290, "Hyderabad": 520, "Kolkata": 1360},
    "Kolkata":   {"Delhi": 1300, "Lucknow": 890, "Hyderabad": 1180, "Chennai": 1360}
}
```

> **Academic Disclaimer:**
> All edge weights represent illustrative sample distances in kilometres (km) chosen for algorithmic demonstration and testing. They are not verified commercial flight nautical miles or live airline schedule data.

---

## 4. DAA Algorithm Implementation (Dijkstra's Algorithm)

### How the Algorithm Works
1. **Initialization:**
   - Tentative distance to the source airport is set to $0$; distances to all other 8 airports are set to $\infty$ (`float('inf')`).
   - A `previous` dictionary maps each vertex to `None` to enable route backtracking.
   - A binary min-heap `priority_queue` is initialized with `(0, source)`.

2. **Greedy Selection & Min-Heap:**
   - At each step, `heapq.heappop()` extracts the unvisited vertex $u$ with the smallest tentative distance in $O(\log V)$.
   - Outdated heap entries with $d > \text{distances}[u]$ are skipped (lazy deletion).
   - If the extracted airport is the destination, the search terminates early with guaranteed optimality.

3. **Edge Relaxation:**
   - For every neighbor $v$ of current airport $u$ with edge weight $w(u, v)$:
     $$\text{If } \text{distances}[u] + w(u, v) < \text{distances}[v]:$$
     $$\text{distances}[v] = \text{distances}[u] + w(u, v)$$
     $$\text{previous}[v] = u$$
     $$\text{heapq.heappush}(\text{priority\_queue}, (\text{distances}[v], v))$$

4. **Path Reconstruction:**
   - Starting from `destination`, the path is traced backward using `previous[curr]` until reaching `source`.
   - Reversing this sequence yields the ordered flight itinerary and individual flight legs.

---

## 5. DAA Complexity Analysis

### Time Complexity: $\mathcal{O}((V + E) \log V)$
- **$V$ (Vertices):** Number of airports in the network ($V = 9$).
- **$E$ (Edges):** Number of bidirectional flight connections ($E = 15$).
- **Heap Operations:**
  - Each vertex is extracted from the binary min-heap at most once: $V \times \mathcal{O}(\log V) = \mathcal{O}(V \log V)$.
  - Each edge is relaxed at most once, performing a heap insertion: $E \times \mathcal{O}(\log V) = \mathcal{O}(E \log V)$.
  - Total time complexity: $\mathcal{O}((V + E) \log V)$.
- **Comparison:** In contrast to an un-optimized array-based Dijkstra ($\mathcal{O}(V^2)$), using Python's `heapq` provides optimal performance on sparse and medium-density graphs.

### Space Complexity: $\mathcal{O}(V + E)$
- **Adjacency List:** $\mathcal{O}(V + E)$ to store 9 vertices and 30 directed edge references.
- **Distances Dictionary:** $\mathcal{O}(V)$ to store the shortest distance to each airport.
- **Predecessor Map (`previous`):** $\mathcal{O}(V)$ to store parent pointers for path reconstruction.
- **Priority Queue Min-Heap:** At most $\mathcal{O}(E)$ elements in the worst case before lazy extraction.
- Total auxiliary space: $\mathcal{O}(V + E)$.

---

## 6. Project Directory Structure

```text
flight_route_planner/
│
├── app.py                  # Flask web server and routing controller
├── algorithm.py            # Graph adjacency list and Dijkstra's algorithm
├── test_algorithm.py       # Unit test suite (unittest framework)
├── requirements.txt        # Python dependency manifest
├── README.md               # Project documentation & DAA analysis
│
├── templates/
│   └── index.html          # Responsive HTML5 dashboard template
│
└── static/
    ├── style.css           # Airline-themed responsive CSS3 styles
    └── script.js           # Vanilla JavaScript for AJAX & UI interaction
```

---

## 7. Installation & Running Instructions (Windows)

Follow these steps in **Visual Studio Code** or PowerShell:

### Step 1: Open the Project Directory
```powershell
cd C:\Users\DELL\Downloads\flight_route_planner
```

### Step 2: Create and Activate a Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application
```powershell
python app.py
```

### Step 5: Open in Web Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

### Step 6: Execute Automated Unit Tests
To run all unit tests:
```powershell
python -m unittest -v test_algorithm.py
```
Or run test discovery:
```powershell
python -m unittest discover
```

---

## 8. Verification & Required Test Outputs

### Test Case 1: Delhi &rarr; Bengaluru
- **Expected Shortest Route:** Delhi &rarr; Jaipur &rarr; Mumbai &rarr; Bengaluru
- **Total Distance:** 1,995 km
- **Airports Visited:** 4
- **Flight Legs:** 3
  - Leg 1: Delhi (DEL) &rarr; Jaipur (JAI) = 280 km
  - Leg 2: Jaipur (JAI) &rarr; Mumbai (BOM) = 1,145 km
  - Leg 3: Mumbai (BOM) &rarr; Bengaluru (BLR) = 570 km
  - **Sum:** $280 + 1,145 + 570 = 1,995\text{ km}$

### Test Case 2: Ahmedabad &rarr; Mumbai
- **Expected Shortest Route:** Ahmedabad &rarr; Mumbai
- **Total Distance:** 440 km
- **Airports Visited:** 2
- **Flight Legs:** 1
  - Leg 1: Ahmedabad (AMD) &rarr; Mumbai (BOM) = 440 km

### Test Case 3: Same Origin and Destination (e.g., Delhi &rarr; Delhi)
- **Expected Route:** Delhi
- **Total Distance:** 0 km
- **Flight Legs:** 0

### Test Case 4: Reverse Path (Bengaluru &rarr; Delhi)
- **Expected Route:** Bengaluru &rarr; Mumbai &rarr; Jaipur &rarr; Delhi
- **Total Distance:** 1,995 km (Confirms undirected graph symmetry)

---

## 9. Viva Voce Questions & Answers

1. **Why is Dijkstra's algorithm preferred over Breadth-First Search (BFS)?**
   - BFS only finds the shortest path in unweighted graphs (where every edge has cost 1). Dijkstra's algorithm accommodates weighted edges representing physical distances.

2. **Why does Dijkstra fail with negative edge weights?**
   - Dijkstra makes greedy choices assuming once a vertex is finalized, no shorter path to it exists. Negative weights violate this assumption; the Bellman-Ford algorithm should be used if negative weights exist.

3. **Why do we use Python's `heapq` module?**
   - A naive search through an array to find the minimum distance takes $\mathcal{O}(V)$ per step, leading to $\mathcal{O}(V^2)$ time. A binary min-heap retrieves and removes the minimum element in $\mathcal{O}(\log V)$, reducing overall complexity to $\mathcal{O}((V + E) \log V)$.

4. **How does edge relaxation work?**
   - If travelling from source to vertex $v$ via intermediate vertex $u$ is shorter than the currently recorded distance to $v$, we update `distances[v] = distances[u] + weight(u, v)` and set `previous[v] = u`.
