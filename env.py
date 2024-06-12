from collections import defaultdict

from nodelist import NodeList
from nodes.control import BranchNode
from nodes.basicmath import AddNode, MinusNode, MultiplyNode, DivideNode, GreaterNode


class Env:
    @staticmethod
    def registerNode():
        NodeList.registerNode([AddNode, MinusNode, MultiplyNode, DivideNode, GreaterNode, BranchNode])

    @staticmethod
    def getRegisteredNode():
        return NodeList._node_list

    @staticmethod
    def getNodeListJson():
        data = defaultdict(dict)
        for cls in Env.getRegisteredNode():
            pkg_name = cls.package_name
            node_title = cls.node_title
            data[pkg_name][node_title] = cls
        return data
