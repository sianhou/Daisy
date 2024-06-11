from nodetable import NodeTable
from nodes.branch_node import BranchNode
from nodes.basicmath import AddNode


class Env:
    @staticmethod
    def registerNode():
        NodeTable.registerNode([AddNode, BranchNode])

    @staticmethod
    def getRegisteredNode():
        return NodeTable.node_table
