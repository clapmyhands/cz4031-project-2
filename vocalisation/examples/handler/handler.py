
class Handler:
    def __init__(self):
        pass

    def handle(self, node):
        pass


class ScanHandler(Handler):
    def __init__(self):
        Handler.__init__(self)
        self.scan_expand = {
            'Seq': 'Sequential'
        }


    def handle(self, node):
        scan_type = self.__expand_scan(node.get('Node Type'))
        relation = node.get('Relation Name')
        alias = node.get('Alias')
        text = "{} in relation '{}' with alias '{}'.".format(scan_type, relation, alias)
        print(text)
        return text


    def __expand_scan(self, node_type):
        tmp = node_type.split(' ')
        expanded = self.scan_expand.get(tmp[0], tmp[0])
        return ' '.join([expanded, tmp[1]])


class LimitHandler(Handler):
    def __init__(self):
        Handler.__init__(self)

    def handle(self, node):
        limit_row = node.get('Actual Rows')
        text = "Result limited to {} row".format(limit_row)
        if limit_row > 1: text += 's'
        text += '.'
        print(text)
        return text


handler = {
    "Limit": LimitHandler(),
    "Seq Scan": ScanHandler()
}

def get_handler_for_nodetype(node_type):
    """
    get handler according to node_type.
    handler.get() will return None if doesn't exist
    :param node_type:
    :return: handler
    """
    return handler.get(node_type)