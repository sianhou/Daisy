from nodelist import NodeList
from nodes.branch_node import BranchNode
from nodes.basicmath import AddNode


class Env:
    @staticmethod
    def registerNode():
        NodeList.registerNode([AddNode, BranchNode])

    @staticmethod
    def getRegisteredNode():
        return NodeList._node_list

    @staticmethod
    def getNodeListJson():
        data = {
            'Basic Operation': {
                'Add': AddNode,
            },
            'Control Structure': {
                'Branch': BranchNode,
            }
        }
        return data
