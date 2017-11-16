from __future__ import print_function



class Handler:
    def __init__(self):
        pass

    def handle(selfs, node):
        pass

    @staticmethod
    def stringify_list(list):
        return [str(i) for i in list]


class ScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)
        self.scan_expand = {
            'Seq': 'Sequential'
        }


    def handle(self, node):
        scan_type = self.__expand_scan(node.get('Node Type'))
        direction = node.get('Scan Direction')
        if direction:
            scan_type += " " + direction

        relation = node.get('Relation Name')

        alias = node.get('Alias')
        if alias and alias != relation:
            relation = "'{}' with alias '{}'".format(relation, alias)

        text = "Do {} in relation {}.".format(scan_type, relation)
        print(text)
        return [text]


    def __expand_scan(self, node_type):
        tmp = node_type.split(" ")
        if tmp[-1] != "Scan":
            tmp.append("Scan")
        tmp[0] = self.scan_expand.get(tmp[0], tmp[0])
        return " ".join(tmp)


class LimitHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        limit_row = node.get('Actual Rows')
        text = "Result is limited to {} row".format(limit_row)
        if limit_row > 1:
            text += 's'
        text += '.'
        print(text)
        return [text]


class SortHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        # node_type = node.get('Node Type')
        sort_method = node.get('Sort Method')
        sort_key = Handler.stringify_list(node.get('Sort Key'))
        text = "Do {} on the result with sort key: {}."\
            .format(sort_method, sort_key)
        print(text)
        return [text]


class HashHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        buckets = node.get('Hash Buckets')
        text = "Hash the result using {} buckets.".format(buckets)
        print(text)
        return [text]


class AggregateHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        node_type = node.get('Node Type')
        strategy = node.get('Strategy')


        group_key = Handler.stringify_list(node.get('Group Key'))
        output = Handler.stringify_list(node.get('Output'))

        aggregate_output = list(set(output)-set(group_key))

        text = "Aggregate the result "
        if aggregate_output:  # if empty aggregate
            text += "get {} ".format(aggregate_output)
        text += "using group key: {}.".format(group_key)
        print(text)
        return [text]



class HandlerWithChilds:
    def __init__(self):
        pass

    def handle_with_childs(self, node, childs):
        pass

    @staticmethod
    def childs_to_string(childs=None):
        if childs:
            if len(childs) == 2:
                return "{} and {}".format(*childs)
            else:
                childs[-1] = "and " + childs[-1]
                return ", ".join(childs)


class AppendHandler(HandlerWithChilds):
    def __init__(self):
        HandlerWithChilds.__init__(self)

    def handle_with_childs(self, node, childs):
        text = "Append: {}.".format(self.childs_to_string(childs))
        print(text)
        return [text]


class HashJoinHandler(HandlerWithChilds):
    def __init__(self):
        HandlerWithChilds.__init__(self)

    def handle_with_childs(self, node, childs):
        node_type = node.get('Node Type')
        join_type = node.get('Join Type')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {}.".format(tmp, self.childs_to_string(childs))
        print(text)
        return [text]


handler = {
    "Limit": LimitHandler(),
    "Seq Scan": ScanHandler(),
    "Bitmap Index Scan": ScanHandler(),
    "Index Only Scan": ScanHandler(),
    "Sort": SortHandler(),
    "Hash": HashHandler(),
    "Aggregate": AggregateHandler(),
    "Append": AppendHandler(),
    "Hash Join": HashJoinHandler()
}

def get_handler_for_nodetype(node_type):
    """
    get handler according to node_type.
    handler.get() will return None if doesn't exist
    :param node_type:
    :return: handler
    """
    return handler.get(node_type)