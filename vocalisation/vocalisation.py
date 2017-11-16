from __future__ import print_function

import json

import handler
import pyttsx3

engine = pyttsx3.init('nsss')

class TempResultCounter:
    def __init__(self):
        self.counter = 0
        self.tr_names = []

    def pushTemp(self, n=None):
        if n is None:
            n = 1
        self.counter += n
        return self.counter

    def resolveTemp(self, n=None):
        if n is None:
            n = 1
        self.counter -= n
        resolved = self.tr_names[-n:]
        self.tr_names = self.tr_names[:-n]
        return resolved

    def get_temp_name(self):
        tr_name = "r{}".format(self.pushTemp())
        self.tr_names.append(tr_name)
        return tr_name


trc = TempResultCounter()

def process_node(node, depth, single_child=True):
    plans = node.get('Plans')
    string_builder = []

    # string_builder.append("Depth: {}".format(depth))

    node_type = node.get('Node Type')
    # string_builder.append("Type: {}".format(node_type))

    # if plans:
    #     string_builder.append("Child: {}".format(len(plans)))

    # output = node.get('Output')
    # if output:
    #     string_builder.append("Output: {}".format(output))

    resolved = None
    child_txt = []
    if plans:
        if len(plans) > 1:
            for plan in plans:
                child_txt.extend(process_node(plan, depth + 1, False))
            resolved = trc.resolveTemp(len(plans))
            # print("Resolved: {}.".format(", ".join(resolved)))
        else:
            for idx, plan in enumerate(plans):
                child_txt.extend(process_node(plan, depth + 1))

    # print(", ".join(string_builder))
    current_txt = []
    handler_class = handler.get_handler_for_nodetype(node_type)
    if handler_class:
        if resolved:
            current_txt = handler_class.handle_with_childs(node, resolved)
        else:
            current_txt = handler_class.handle(node)

    if child_txt: string_builder.extend(child_txt)
    if current_txt: string_builder.extend(current_txt)
    if not single_child:
        temp_result_txt = "Keep temporary result as {}.".format(trc.get_temp_name())
        print(temp_result_txt)
        string_builder.append(temp_result_txt)
    return string_builder


def filter_tree(qep):
    root = {}
    plan = qep[0].get('Plan')
    plan_list = process_node(plan, 0)
    final_plan = " ".join(plan_list)
    engine.say(final_plan)
    engine.runAndWait()



def main(filename):
    # engine.say(filename)
    # engine.runAndWait()
    with open(filename, 'r') as my_file:
        qep = json.load(my_file)#, object_pairs_hook=OrderedDict)
    print(qep[0]['Plan'])
    filter_tree(qep)

if __name__ == '__main__':
    main('./examples/long.json')