# coding: utf-8

class NodeList:
    _node_list = []

    @staticmethod
    def registerNode(node):
        if isinstance(node, list):
            NodeList._node_list.extend(node)
        else:
            NodeList._node_list.append(node)
