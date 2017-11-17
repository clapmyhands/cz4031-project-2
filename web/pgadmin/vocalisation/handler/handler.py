from __future__ import print_function



class Handler:
    def __init__(self):
        pass

    def handle(self, node, childs):
        pass

    @staticmethod
    def stringify_list(list=None):
        if list is None:
            list = []

        my_list = [str(i) for i in list]
        return my_list

    @staticmethod
    def list_to_string(childs=None):
        if childs:
            if len(childs) == 1:
                return childs[0]
            elif len(childs) == 2:
                return "{} and {}".format(*childs)
            else:
                childs[-1] = "and " + childs[-1]
                return ", ".join(childs)


class ScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)
        self.scan_expand = {
            'Seq': 'Sequential'
        }


    def handle(self, node, childs):
        scan_type = self.__expand_scan(node.get('Node Type'))
        direction = node.get('Scan Direction')
        if direction:
            scan_type += " " + direction
        text = "Do {}".format(scan_type)

        relation = node.get('Relation Name')
        if relation:
            text += " in relation '{}'".format(relation)

        alias = node.get('Alias')
        if alias and alias != relation:
            text += " with alias '{}'".format(alias)

        cond = node.get('Filter', node.get('Index Cond'))
        if cond:
            text += " with condition: {}".format(cond)

        index_name = node.get('Index Name')
        if index_name:
            text += " with index '{}'".format(index_name)

        text += '.'

        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text

        print(text)
        return [text]


    def __expand_scan(self, node_type):
        tmp = node_type.split(" ")
        if tmp[-1] != "Scan":
            tmp.append("Scan")
        tmp[0] = self.scan_expand.get(tmp[0], tmp[0])
        return " ".join(tmp)


class BitmapHeapScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        direction = node.get('Scan Direction')
        if direction:
            node_type += " " + direction
        relation = node.get('Relation Name')
        text = "Use index to do {} in relation '{}'".format(node_type, relation)

        alias = node.get('Alias')
        if alias and alias != relation:
            text += " with alias '{}'".format(alias)

        cond = node.get('Filter')
        if cond:
            text += " with condition: {}".format(cond)

        index_name = node.get('Index Name')
        if index_name:
            text += " with index '{}'".format(index_name)

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class BitmapIndexScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        direction = node.get('Scan Direction')
        if direction:
            node_type += " " + direction
        index_name = node.get('Index Name')
        text = 'Do {} on {}'.format(node_type, index_name)

        index_cond = node.get('Index Cond')
        if index_cond:
            text += ' with condition: {}'.format(index_cond)

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class SubqueryScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        scan_type = node.get('Node Type')

        alias = node.get('Alias')

        text = "Do {} on result ".format(scan_type, alias)

        if alias:
            text += "and use {} as alias".format(alias)
        text += "."
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class FunctionScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')

        pass


class ValuesScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        text = 'Do {}'.format(node_type)

        alias = node.get('Alias')
        if alias:
            text += " with alias '{}'".format(alias)

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class CTEScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        cte_name = node.get('CTE Name')
        text = 'Do {} on CTE {}'.format(node_type, cte_name)

        alias = node.get('Alias')
        if alias and alias != cte_name:
            text += " with alias '{}'".format(alias)

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class SampleScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        relation = node.get('Relation Name')

        text = "{} on relation '{}'".format(node_type, relation)

        method = node.get('Sampling Method')
        if method:
            text = "{} {}".format(method, text)

        alias = node.get('Alias')
        if alias and alias != relation:
            text += " with alias '{}'".format(alias)

        parameter = node.get('Sampling Parameters')
        parameter = Handler.stringify_list(parameter)
        if parameter:
            text += " with parameter: {}".format(Handler.list_to_string(parameter))

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class TidScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        relation = node.get('Relation Name')

        text = "{} on relation '{}'".format(node_type, relation)

        alias = node.get('Alias')
        if alias and alias != relation:
            text += " with alias '{}'".format(alias)

        cond = node.get('Filter', node.get('TID Cond'))
        if cond:
            text += " with condition: {}".format(cond)

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]
        pass


class LimitHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        limit_row = node.get('Actual Rows')
        text = "Result is limited to {} row".format(limit_row)
        if limit_row > 1:
            text += 's'
        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class SortHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        # node_type = node.get('Node Type')
        sort_method = node.get('Sort Method')
        sort_key = Handler.stringify_list(node.get('Sort Key'))
        space_type = node.get('Sort Space Type')
        if sort_method is None:
            sort_method = "Sort"
        text = "Do {} on the result with sort key: {}"\
            .format(sort_method, sort_key)
        if space_type:
            text += " in {}".format(space_type)
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        text += "."
        print(text)
        return [text]


class HashHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        buckets = node.get('Hash Buckets')
        text = "Hash the result using {} buckets.".format(buckets)
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class AggregateHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        strategy = node.get('Strategy')
        node_type = "{} {}".format(strategy, node_type)


        group_key = Handler.stringify_list(node.get('Group Key'))
        output = Handler.stringify_list(node.get('Output'))

        text = "Do {} on the result".format(node_type)

        if output:
            text += " to get {}".format(Handler.list_to_string(output))

        if group_key:
            text += " using group key: {}".format(Handler.list_to_string(group_key))
        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class AppendHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        text = "{}: {}.".format(node_type, self.list_to_string(childs))
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class HashJoinHandler(Handler):
    def __init__(self):
        Handler.__init__(self)


    def handle(self, node, childs):
        node_type = node.get('Node Type')
        join_type = node.get('Join Type')
        join_cond = node.get('Hash Cond')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {} with condition: {}.".format(tmp, self.list_to_string(childs), join_cond)
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class NestedLoopJoinHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        join_type = node.get('Join Type')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {}".format(tmp, self.list_to_string(childs))

        join_cond = node.get('Join Filter')
        if join_cond:
            text += " with condition: {}".format(join_cond)

        text += '.'
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class MergeJoinHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        join_type = node.get('Join Type')
        join_cond = node.get('Merge Cond')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {} with condition: {}.".format(tmp, self.list_to_string(childs), join_cond)
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class UniqueHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        attribute_name = None
        output = node.get('Output')
        if output:
            attribute_name = node.get('Output')[0]
        text = "Take unique values"
        if attribute_name:
            text += " of {}".format(attribute_name)
        text += " from result."
        subplan = node.get('Subplan Name')
        if subplan:
            text += "Create {} by ".format(subplan) + text
        print(text)
        return [text]


class DeleteHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        relation = node.get('Relation Name')
        text = "Delete result from relation {}.".format(relation)
        print(text)
        return [text]


class InsertHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        # node_type = node.get('Node Type')
        text = 'Insert result'

        relation = node.get('Relation Name')
        if relation:
            text += " to relation '{}'".format(relation)

        text += '.'
        print(text)
        return [text]


class UpdateHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        relation = node.get('Relation Name')
        text = "Update result from relation {}.".format(relation)
        print(text)
        return [text]


class BitmapHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        tmp = ' '.join((node_type[:6], node_type[6:]))  # Bitmap --> 6 char
        text = 'Do {} on {}'.format(tmp, self.list_to_string(childs))
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        text += '.'
        print(text)
        return [text]


class MaterializeHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        text = '{} the result'.format(node_type)
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        text += '.'
        print(text)
        return [text]


class ResultHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')
        text = "{}".format(node_type)

        output = Handler.stringify_list(node.get('Output'))
        if output:
            text += " with output: {}".format(Handler.list_to_string(output))

        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        text += '.'
        print(text)
        return [text]


class SetOpHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        command = node.get('Command')
        strategy = node.get('Strategy')
        node_type = '{} Set Operator {}'.format(strategy, command)

        text = 'Do {} on result'.format(node_type)
        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text
        text += '.'
        print(text)
        return [text]


class GroupHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        text = 'Group result'

        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text

        group_key = Handler.stringify_list(node.get('Group Key'))
        if group_key:
            text += ' on group key: {}'.format(Handler.list_to_string(group_key))
        text += '.'

        print(text)
        return [text]


class GatherMergeHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        pass


class WindowAggHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')

        text = "Window Aggregate the result"

        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text

        text += '.'

        print(text)
        return [text]

class RecursiveUnionHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        node_type = node.get('Node Type')

        text = "Recursive Union the result"

        subplan = node.get('Subplan Name')
        if subplan:
            text = "Create {} by ".format(subplan) + text

        text += '.'

        print(text)
        return [text]


class LockRowsHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node, childs):
        text = "Lock the rows of the result."
        print(text)
        return [text]


handler = {
    "Materialize": MaterializeHandler(),
    "Limit": LimitHandler(),
    "Seq Scan": ScanHandler(),
    "Bitmap Index Scan": BitmapIndexScanHandler(),
    "Bitmap Heap Scan": BitmapHeapScanHandler(),
    "Index Scan": ScanHandler(),
    "Index Only Scan": ScanHandler(),
    "Subquery Scan": SubqueryScanHandler(),
    "Function Scan": FunctionScanHandler(),
    "Values Scan": ValuesScanHandler(),
    "CTE Scan": CTEScanHandler(),
    "Sample Scan": SampleScanHandler(),
    "Tid Scan": TidScanHandler(),
    "WorkTable Scan": ScanHandler(),
    "Foreign Scan": ScanHandler(),
    "Custom Scan": ScanHandler(),
    "WindowAgg": WindowAggHandler(),
    "Sort": SortHandler(),
    "Hash": HashHandler(),
    "Aggregate": AggregateHandler(),
    "Append": AppendHandler(),
    "Merge Append": AppendHandler(),
    "Hash Join": HashJoinHandler(),
    "Nested Loop": NestedLoopJoinHandler(),
    "Merge Join": MergeJoinHandler(),
    "Unique": UniqueHandler(),
    "BitmapAnd": BitmapHandler(),
    "BitmapOr": BitmapHandler(),
    "Delete": DeleteHandler(),
    "Insert": InsertHandler(),
    "Update": UpdateHandler(),
    "Result": ResultHandler(),
    "SetOp": SetOpHandler(),
    "Group": GroupHandler(),
    "Gather Merge": GatherMergeHandler(),
    "Recursive Union": RecursiveUnionHandler(),
    "LockRows": LockRowsHandler()
}

def get_handler_for_nodetype(node_type):
    """
    get handler according to node_type.
    handler.get() will return None if doesn't exist
    :param node_type:
    :return: handler
    """
    return handler.get(node_type)