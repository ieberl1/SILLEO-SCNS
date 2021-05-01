import networkx as nx
import os
from pathlib import Path

graphs = []
#city_names = []
#ground_stations_file='city_data.txt'


# def set_city_names(city_names_file_str):
#     data = []
#     cities_str = []
#     with open(city_names_file_str, 'r') as f:
#         for line in f:
#             my_line = []
#             for word in line.split():
#                 my_line.append(word)
#             data.append(my_line)
#     for i in range(1, len(data)):
#         self.city_names.append(data[i][0])
#         self.model.addGroundPoint(float(data[i][1]), float(data[i][2]))


def get_graphs(directory):
    num_graphs = 0
    if os.path.isdir(directory):
        for gml in Path(directory).glob('**/*.gml'):
            print("Importing " + str(gml))
            graphs.append(nx.read_gml(gml))
            num_graphs += 1
        print("Imported %s graphs" % num_graphs)


def get_shortest_path(graph, n1_lbl, n2_lbl):
    path_links = None
    # run dijkstra's between two points
    if None in [graph, n1_lbl, n2_lbl]:
        print("Cannot get shortest path. Invalid parameter")
        return

    # run shortest path, handle exception if path not exist
    try:
        path = nx.shortest_path(
            graph,
            source=str(n1_lbl),
            target=str(n2_lbl),
            weight='distance')

        print("Path is :" + str(path))
        path_links = []

        # convert list of nodes into edges
        for i in range(len(path) - 1):
            path_links.append([path[i], path[i + 1]])
        print("Path links: " + str(path_links))

    except nx.exception.NetworkXNoPath:
        print("path does not exist...")

    return path_links


def get_total_distance(graph, links):
    total_distance = 0
    for link in links:
        link_distance = graph[link[0]][link[1]]['distance']
        print("Current link distance: " + str(link_distance))
        total_distance += link_distance
    print("Total Distance: " + str(total_distance))
    return total_distance


def calculate_latency(graph, n1_lbl, n2_lbl):
    path_links = get_shortest_path(graph, n1_lbl, n2_lbl)
    num_hops = len(path_links)
    total_distance = get_total_distance(graph, path_links)
    # latency = (path length in meters / c) + queuing delay
    # c: 3E8 or 300000000 meters/sec
    # queuing delay: 2 microseconds per hop
    latency = (total_distance / 300000000) + (0.000002 * num_hops)
    print("Latency is: %s" % latency)
    return latency


def get_city_label(graph, city_str):
    label = "No label found"
    for n in graph.nodes(data='placeName'):
        if n[1] == city_str:
            label = n[0]
            break
    print("Returning: %s of type %s" % (str(label), type(label)))
    return label


if __name__ == "__main__":
    #set_city_names(ground_stations_file)
    g = nx.read_gml("gmls/g_0000055.gml")
    get_graphs("./gmls")
    #calculate_latency("DC", "Rome")
    print("Num graphs: " + str(len(graphs)))
    print("Graph1: ")
    print(graphs[0].nodes())
    node1_lbl = get_city_label(graphs[0], "DC")
    node2_lbl = get_city_label(graphs[0], "Rome")
    calculate_latency(graphs[0], node1_lbl, node2_lbl)



