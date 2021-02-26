import json
import math
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing


class Place:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def getPlaces():
    with open('addresses.json') as json_file:
        data = json.load(json_file)
        students = list()

        for student in data:
            s = Place(student['x'], student['y'])

            students.append(s)

        return students

### Google OR-Tools attempt ###
# https://developers.google.com/optimization/routing/tsp
def create_data_model(places):
    """Stores the data for the problem."""
    data = {}
    distance_matrix = np.empty((30, 30))
    for i in range(len(places)):
        for j in range(len(places)):
            distance_matrix[i][j] = d(places[i], places[j])
    data['distance_matrix'] = distance_matrix.tolist()
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def d(p1, p2):
    return math.sqrt(((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2))

data = create_data_model(getPlaces())
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                       data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)
def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
search_parameters.time_limit.seconds = 10  # Change run time
search_parameters.log_search = True

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

solution = routing.SolveWithParameters(search_parameters)
if solution:
    print_solution(manager, routing, solution)

# We get a score of 1422km (0.70323)
# Issue is, the teacher returns from node 13 to node 0 at the end, which the problem doesn't require.
# This distance (64,04594km) can be subtracted from our solution, giving a solution of 1358 (0.74)
# Clearly, the starting point is wrong. TODO find out how to find the optimal starting point


# places = getPlaces()
# distance_matrix = np.empty((30, 30))
# for i in range(len(places)):
#     for j in range(len(places)):
#         distance_matrix[i][j] = d(places[i], places[j])
#
#
# permutation, distance = solve_tsp_simulated_annealing(distance_matrix)
# print(permutation)
# print(distance)



#
# import matplotlib.pyplot as plt
#
# x,y = [], []
# for place in getPlaces():
#     x.append(place.x)
#     y.append(place.y)
# # Plot
# plt.scatter(x, y)
# plt.show()
