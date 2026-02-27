# Case Study Analysis: Night Economy Taxi Agent in Grid-London

**Student Name:** Baburam Bastola  
**Student ID:** A00022220  
**Module:** Artificial Intelligence (CMP-N206-0)  
**Programme:** BSc Computer Science  
**University:** University of Roehampton  

---

## 1. Introduction: The Agent-Environment Paradigm
The formulation of real-world decision-making problems in Artificial Intelligence is fundamentally framed around the agent-environment interaction paradigm. As defined by Russell and Norvig, an agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators. Rationality, in this context, is the property of an agent that acts so as to achieve the best outcome or, when there is uncertainty, the best expected outcome given its percepts and internal knowledge.

This case study analysis focuses on the design, implementation, and evaluation of a **Multi-Agent System (MAS)** "Night Economy Taxi Fleet" operating within a simplified "Grid-London". The night economy presents unique challenges for autonomous agents: increased traffic closures, variable demand hotspots (surge zones), and specific passenger characteristics such as intoxication, which impact operational efficiency. By framing this as a cooperative rational agent problem, we can evaluate how a fleet of taxis coordinates via a centralized dispatcher to optimize urban transport.

## 2. Scenario and Environment Model
### 2.1 The Grid-London Environment
The environment is modelled as a 10×10 discrete grid representing a simplified map of central London during peak night hours (Friday and Saturday, 22:00–04:00). Each cell $(r, c)$ represents a specific location. The environment is classified as:
- **Partially Observable:** The agents know the environment map but only perceive passenger details upon assignment.
- **Stochastic:** Passenger spawn locations and sobriety status are determined by probabilistic distributions.
- **Sequential:** Current actions (e.g., fuel spent) impact the total utility of the session.
- **Static:** While the agents move, the grid structure (road closures) remains fixed for the duration of a specific scenario.
- **Discrete:** Actions and locations are defined in finite steps.
- **Multi-Agent:** The simulation features a fleet of taxis coordinating via a centralized dispatcher to serve multiple passengers.

The grid contains four cell types:
1. **Normal Road (0):** Standard navigable streets with a unit movement cost.
2. **Blocked Cells (1):** Representing road closures, dense crowds at club entrances, or police cordons. These are impassable.
3. **Hotspot Zones (2):** Areas of high demand such as Soho, Shoreditch, Camden, and Brixton. Pickups here yield a "surge bonus".
4. **Home Zones (3):** Residential drop-off points like Islington, Hackney, and Clapham.

![FIGURE 1 — Wireframe: Night Economy Taxi Agent Interface](file:///Users/mqc/Desktop/AI%20COURSE%20WORK%20/assets/wireframe.png)
*Figure 1: Wireframe depicting the structural layout of the Night Economy Taxi Agent interface, including the 10x10 Grid-London map, scenario controls, and live step log.*

### 2.2 Assumptions
- All moves between adjacent cells have a uniform distance.
- The agent has a perfect map of all road closures at the start of a trip.
- A "drunk" passenger status is a binary state that causes a fixed delay during the pickup phase.

## 3. Agent Design and Percepts
The Night Economy Taxi Agent is a **goal-based rational agent**. It does not simply react to the nearest cell; it maintains an internal model of the passenger's destination and plans a sequence of actions (a path) to achieve that goal.

### 3.1 Percepts (Sensors)
The agent perceives the following data at each time step $t$:
- **Current Location:** $(r_{taxi}, c_{taxi})$.
- **Passenger Location:** $(r_{p}, c_{p})$ (available once assigned).
- **Passenger Destination:** $(r_{d}, c_{d})$.
- **Blocked Roads:** A set of coordinates representing all impassable cells.
- **Utility Score:** Its cumulative performance metric.

### 3.2 Actions (Actuators)
The agent can execute a finite set of actions $A = \{Move North, Move South, Move East, Move West, Pick Up, Drop Off\}$. Each movement action transitions the agent between grid coordinates, while pickup/dropoff actions change the agent's internal state (carrying passenger).

![FIGURE 3 — Use Case Diagram: Night Economy Taxi Agent](file:///Users/mqc/Desktop/AI%20COURSE%20WORK%20/assets/use_case_diagram.png)
*Figure 2: Use Case Diagram illustrating the core interactions between the TaxiAgent actor and the System Boundary of the Grid-London environment.*

![FIGURE 4 — Entity Relationship Diagram: Night Economy Taxi Agent](file:///Users/mqc/Desktop/AI%20COURSE%20WORK%20/assets/erd.png)
*Figure 3: Entity Relationship Diagram (ERD) showing the data architecture of the simulation, including relations between the TaxiAgent, GridWorld, Passengers, and logs.*

## 4. Performance Measure (Utility Function)
The performance measure is the objective criterion for success. For the taxi agent, rationality is defined as the maximisation of this utility function $U$. We define $U$ as follows:

| Event | Score Change | Justification |
| :--- | :--- | :--- |
| **Successful Drop-off** | +20 | Mirrors the primary revenue/fare from a trip. |
| **Movement (Fuel/Time)** | -1 | Penalises inefficiency and models carbon emissions [5]. |
| **Blocked Road Collision**| -5 | Penalises dangerous or illegal maneuvers. |
| **Surge Zone Pickup** | +5 | Models higher profitability in high-demand areas. |
| **Drunk Passenger Delay** | -2 | Models the time/opportunity cost of assisting intoxicated riders [2]. |
| **Session Completion** | +10 | Bonus for completing 3 trips, rewarding sustained productivity. |

**Rational Rationale:** This measure makes sense because it balances the need for revenue (+20) against the operational costs of the vehicle (-1 per move). By penalising collisions (-5) more heavily than movement, we ensure the agent avoids "shortcuts" through blocked areas. The surge bonus incentivises positioning near hotspots, while the drunk passenger penalty reflects real-world findings by the GLA that late-night service to intoxicated individuals takes ~20% longer per pickup [2].

## 5. Decision-Making Method: Search Strategies
To find the optimal path to goals, the agent employs two search strategies: Breadth-First Search (BFS) and A* Search.

### 5.1 Breadth-First Search (BFS)
BFS is an uninformed search that explores the state space layer by layer.
- **Why it works well:** In an unweighted grid (where every move costs exactly -1), BFS is guaranteed to find the shortest path. It is complete and optimal.
- **When it fails:** BFS becomes computationally expensive as the grid size or branching factor increases, as it explores all directions equally (O(b^d)).

### 5.2 A* Search
A* is an informed search using the evaluation function $f(n) = g(n) + h(n)$, where $g(n)$ is the cost to reach the node and $h(n)$ is the **Manhattan Distance** heuristic.
- **Why it works well:** By using a heuristic, A* "guides" the search toward the goal, significantly reducing the number of nodes explored compared to BFS. In Grid-London, the Manhattan distance is an **admissible heuristic** (it never overestimates the distance), ensuring optimality.
- **When it fails:** If the heuristic is poorly chosen or if the environment has complex "U-shaped" obstacles that mislead the heuristic, A* can still be slow, though it remains superior to BFS in most grid scenarios.

![FIGURE 2 — Activity Diagram: TaxiAgent Decision Loop](file:///Users/mqc/Desktop/AI%20COURSE%20WORK%20/assets/activity_diagram.png)
*Figure 4: Activity Diagram depicting the decision loop of the TaxiAgent, from initialization through passenger spawning and path planning to session completion.*

## 6. Evaluation and Results
We conducted three evaluation scenarios to test the agent's rationality across different environmental constraints.

### 6.1 Results Table
The following metrics were captured during simulation runs:

| Scenario | Search | Trips | Parallel Steps | Total Score | Goal Achieved |
| :--- | :--- | :--- | :--- | :--- | :--- |
| S1: Normal Friday | BFS | 1 | 25 | 0 | YES |
| S2: Heavy Closures | BFS | 1 | 19 | 6 | YES |
| S3: Surge Night | A* | 3 | 43 | 42 | YES |
| S4: MAS Fleet | A* | 4 | 30 | 23 | YES |

![FIGURE 6 — Sequence Diagram: One Complete Trip (Scenario 1)](file:///Users/mqc/Desktop/AI%20COURSE%20WORK%20/assets/sequence_diagram.png)
*Figure 5: Sequence Diagram illustrating the synchronous interactions between the TaxiAgent, GridWorld, search algorithms, and Passenger objects during a single trip.*

### 6.2 Analysis of Scenarios
- **Scenario 1 (Baseline):** The agent navigated from its start position to a hotspot pickup and then to a residential home zone. The total movement cost (25 moves) exactly cancelled out the revenue (+20) and surge bonus (+5), resulting in a break-even score of 0. This demonstrates basic rationality: the agent reached the goal via the shortest path but faced a long-distance trip.
- **Scenario 2 (Constraints):** despite having double the road closures, the agent found a path. Interestingly, because the passenger spawned closer to the agent's start point in this specific random seed, the score was higher (+6) despite the obstacles. This highlights that environmental "luck" (stochasticity) impacts single-run performance.
- **Scenario 3 (Productivity):** Using A* search, the agent completed a full 3-trip session. The high score of +42 proves that a rational agent can remain profitable even with delays.
- **Scenario 4 (Fleet Efficiency):** In the Multi-Agent System (MAS) run, two taxis managed 4 passengers. While individual scores were lower due to the random spawn locations, the **parallel time** (maximum steps taken by any one agent) was reduced to just **30 steps**. This demonstrates that MAS coordination via centralized dispatch significantly improves response times and throughput in smart city logistics.

## 7. Explainability: "Why did you choose that move?"
Modern AI must be transparent. The agent includes an explainability module that logs justifications for its actions:
- **Example 1:** "I moved East because the Manhattan distance to the Soho hotspot is currently at its minimum, and it is the only unblocked direction."
- **Example 2:** "I moved North to bypass the road closure at (4,5), as BFS has identified this as the shortest surviving path to the passenger."
By providing these justifications, the agent fulfills the requirements for "Trustworthy AI" as outlined by the European Commission [3], ensuring that human operators can audit the taxi's decisions.

## 8. Reflection on Rationality, Fairness, and Sustainability
### 8.1 Computational Rationality vs. Real-World Rationality
In the 10x10 grid, the agent's rationality is absolute because the state space is small enough for BFS/A* to find the global optimum. However, in a real 1-million-node London street graph, the agent might need to use "bounded rationality"—satisficing with a "good enough" path to save on computation time (energy).

### 8.2 Fairness and Inclusivity
A significant risk in our utility function is the **Geographic Bias** created by surge bonuses. If the agent earns +5 in Soho but 0 in less affluent boroughs, a perfectly rational agent will "starve" the poorer areas of service. This mirrors real-world algorithmic discrimination observed in rideshare platforms [4]. To ensure **Inclusivity**, a more advanced model would remove the -2 drunk passenger penalty. Penalising the service of vulnerable (intoxicated) passengers is ethically questionable, as it might lead the AI to avoid those who most need a safe ride home.

### 8.3 Sustainability
The -1 move cost is a direct **Carbon Signal**. By minimising steps, the agent is inherently minimising its environmental footprint. In future iterations, we could vary this cost based on vehicle type (e.g., -0.1 for an EV vs -1.5 for a diesel taxi), further aligning AI rationality with global sustainability goals [5].

## 9. Conclusion
The Night Economy Taxi Agent demonstrates that a rational, goal-based system can effectively navigate a constrained urban environment. By implementing A* search with a well-justified utility function, the agent achieved high performance while maintaining explainability. However, the study also reveals that "perfect" technical rationality must be tempered with ethical considerations regarding fairness and social responsibility to be truly viable in a modern smart city.

---

## References (IEEE Style)
[1] S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. Hoboken, NJ: Pearson, 2020.  
[2] GLA Economics, "London's Night-Time Economy," Greater London Authority, London, 2017. . Available: https://www.london.gov.uk  
[3] European Commission, "Ethics Guidelines for Trustworthy AI," High-Level Expert Group on Artificial Intelligence, Brussels, 2019.  
[4] K. Lum and W. Isaac, "To predict and serve?," *Significance*, vol. 13, no. 5, pp. 14–19, 2016.  
[5] Transport for London, "Zero Emission Capable Taxis," TfL, London, 2023. . Available: https://tfl.gov.uk  
[6] P. Hart, N. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100–107, 1968.  

---
**Baburam Bastola | A00022220 | CMP-N206-0 AI Assessment**
