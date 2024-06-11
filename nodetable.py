# coding: utf-8

class NodeTable:
    node_table = []

    @staticmethod
    def registerNode(node):
        if isinstance(node, list):
            NodeTable.node_table.extend(node)
        else:
            NodeTable.node_table.append(node)
