from __future__ import print_function



class Handler:
    def __init__(self):
        pass

    def handle(self, node):
        pass

    @staticmethod
    def stringify_list(list=None):
        if list is None:
            list = []

        my_list = [str(i) for i in list]
        return my_list


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
        text = "Do {} in relation '{}'".format(scan_type, relation)

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

    def handle(self, node):
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
        print(text)
        return [text]


class BitmapIndexScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
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
        print(text)
        return [text]


class SubqueryScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        scan_type = node.get('Node Type')

        alias = node.get('Alias')

        text = "Do {} on result ".format(scan_type, alias)

        if alias:
            text += "and use {} as alias".format(alias)
        text += "."
        print(text)
        return [text]


class FunctionScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        node_type = node.get('Node Type')

        pass


class ValuesScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        node_type = node.get('Node Type')
        text = 'Do {}'.format(node_type)

        alias = node.get('Alias')
        if alias:
            text += " with alias '{}'".format(alias)

        text += '.'
        print(text)
        return [text]


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
        space_type = node.get('Sort Space Type')
        text = "Do {} on the result with sort key: {} in {}."\
            .format(sort_method, sort_key, space_type)
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
        node_type = "{} {}".format(strategy, node_type)


        group_key = Handler.stringify_list(node.get('Group Key'))
        output = Handler.stringify_list(node.get('Output'))

        text = "Do {} on the result".format(node_type)

        if output:
            text += " to get {}".format(output)

        if group_key:
            text += " using group key: {}".format(group_key)
        text += '.'
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
        join_cond = node.get('Hash Cond')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {} with condition: {}.".format(tmp, self.childs_to_string(childs), join_cond)
        print(text)
        return [text]


class NestedLoopJoinHandler(HandlerWithChilds):
    def __init__(self):
        HandlerWithChilds.__init__(self)

    def handle_with_childs(self, node, childs):
        node_type = node.get('Node Type')
        join_type = node.get('Join Type')
        join_cond = node.get('Join Filter')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {} with condition: {}.".format(tmp, self.childs_to_string(childs), join_cond)
        print(text)
        return [text]


class MergeJoinHandler(HandlerWithChilds):
    def __init__(self):
        HandlerWithChilds.__init__(self)

    def handle_with_childs(self, node, childs):
        node_type = node.get('Node Type')
        join_type = node.get('Join Type')
        join_cond = node.get('Merge Cond')
        tmp = node_type.split(" ")
        tmp = " ".join((tmp[0],join_type,tmp[1]))
        text = "{} on {} with condition: {}.".format(tmp, self.childs_to_string(childs), join_cond)
        print(text)
        return [text]


class UniqueHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        attribute_name = node.get('Output')[0]
        text = "Take unique values of {} from result.".format(attribute_name)
        print(text)
        return [text]


class DeleteHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        relation = node.get('Relation Name')
        text = "Delete result from relation {}.".format(relation)
        print(text)
        return [text]


class InsertHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
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

    def handle(self, node):
        pass


class BitmapHandler(HandlerWithChilds):
    def __init__(self):
        HandlerWithChilds.__init__(self)

    def handle_with_childs(self, node, childs):
        node_type = node.get('Node Type')
        tmp = ' '.join((node_type[:6], node_type[6:]))  # Bitmap --> 6 char
        text = 'Do {} on {}'.format(tmp, self.childs_to_string(childs))
        text += '.'
        print(text)
        return [text]


class MaterializeHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        node_type = node.get('Node Type')
        text = '{} the result'.format(node_type)
        text += '.'
        print(text)
        return [text]


class ResultHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        node_type = node.get('Node Type')
        text = "{}".format(node_type)

        output = Handler.stringify_list(node.get('Output'))
        if output:
            text += " with output: {}".format(output)

        text += '.'
        print(text)
        return [text]


handler = {
    "Materialize": MaterializeHandler(),
    "Limit": LimitHandler(),
    "Seq Scan": ScanHandler(),
    "Bitmap Index Scan": BitmapIndexScanHandler(),
    "Bitmap Heap Scan": BitmapHeapScanHandler(),
    "Index Only Scan": ScanHandler(),
    "Subquery Scan": SubqueryScanHandler(),
    "Function Scan": FunctionScanHandler(),
    "Values Scan": ValuesScanHandler(),
    "Sort": SortHandler(),
    "Hash": HashHandler(),
    "Aggregate": AggregateHandler(),
    "Append": AppendHandler(),
    "Hash Join": HashJoinHandler(),
    "Nested Loop": NestedLoopJoinHandler(),
    "Merge Join": MergeJoinHandler(),
    "Unique": UniqueHandler(),
    "BitmapAnd": BitmapHandler(),
    "BitmapOr": BitmapHandler(),
    "Delete": DeleteHandler(),
    "Insert": InsertHandler(),
    "Update": UpdateHandler(),
    "Result": ResultHandler()
}

def get_handler_for_nodetype(node_type):
    """
    get handler according to node_type.
    handler.get() will return None if doesn't exist
    :param node_type:
    :return: handler
    """
    return handler.get(node_type)