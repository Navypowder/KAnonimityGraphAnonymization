import sys
import os
import csv
import random


def main(max_node, min_edge, max_edge, file_to_read):

    if os.path.exists(file_to_read):
        csv_file = open(file_to_read, mode='r')
        csv_reader = csv.DictReader(csv_file)
        list_names = list()

        for row in csv_reader:
            list_names.append(row["name"])

        node_to_start = random.sample(list_names, max_node)
        node_to_list_link = dict((name, list()) for name in node_to_start)
        node_to_max_edge = dict((name, 0) for name in node_to_start)

        for node in node_to_list_link.keys():
            max_edge_to_add = random.randint(min_edge, max_edge)
            node_to_max_edge[node] = max_edge_to_add

        for node in node_to_list_link.keys():
            if len(node_to_list_link[node]) < node_to_max_edge[node]:
                link_to_add = random.sample(
                    node_to_start, node_to_max_edge[node] - len(node_to_list_link[node]))
                if node in link_to_add:
                    link_to_add.remove(node)
                for link in link_to_add:
                    if link not in node_to_list_link[node] and \
                            len(node_to_list_link[link]) + 1 <= node_to_max_edge[link]:
                        node_to_list_link[node].append(link)
                        node_to_list_link[link].append(node)

        file_graph = open("graph_friend_{0}_{1}_{2}.csv".format(max_node,min_edge,max_edge), "w")

        for node in node_to_list_link.keys():
            string_to_write = ",".join(node_to_list_link[node])
            string_to_write = node + "," + string_to_write + "\n"
            file_graph.write(string_to_write)

        file_graph.close()
        print("File {0} succesfully created".format(file_graph.name))
    else:
        print("File {} not found".format(file_to_read))


if __name__ == "__main__":
    if len(sys.argv) == 5:

        if int(sys.argv[1]) < 14675 and int(sys.argv[1]) >= int(sys.argv[2]) \
                and int(sys.argv[2]) < int(sys.argv[3]):
            main(int(sys.argv[1]), int(sys.argv[2]),
                 int(sys.argv[3]), sys.argv[4])

        else:
            print("Check value parameters")
    else:
        print("[*]Usage: python max_node min_edge max_edge file_csv_to_read")
