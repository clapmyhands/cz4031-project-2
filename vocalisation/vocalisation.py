from __future__ import print_function


import json

from collections import OrderedDict
from handler import get_handler_for_nodetype


def process_node(node, depth):
    plans = node.get('Plans')
    string_builder = []

    string_builder.append("Depth: {}".format(depth))

    node_type = node.get('Node Type')
    string_builder.append("Type: {}".format(node_type))

    # if plans:
    #     string_builder.append("Child: {}".format(len(plans)))

    # output = node.get('Output')
    # if output:
    #     string_builder.append("Output: {}".format(output))

    print(", ".join(string_builder))
    handler_class = get_handler_for_nodetype(node_type)
    if handler_class:
        handler_class.handle(node)

    if plans:
        for plan in plans:
            process_node(plan, depth+1)


def filter_tree(qep):
    root = {}
    plan = qep[0].get('Plan')
    process_node(plan, 0)


def main(filename):
    with open(filename, 'r') as my_file:
        qep = json.load(my_file)#, object_pairs_hook=OrderedDict)
    print(qep[0]['Plan'])
    filter_tree(qep)

if __name__ == '__main__':
    main('./examples/short_select.json')