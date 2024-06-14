import sys
from collections import defaultdict

from node.nlist import NodeList
from node.op.control import BranchNode
from node.op.basicmath import AddNode, MinusNode, MultiplyNode, DivideNode, GreaterNode
import inspect
import node
from vg_node import Node


class Env:
    @staticmethod
    def registerNode():
        # NodeList.registerNode([AddNode, MinusNode, MultiplyNode, DivideNode, GreaterNode, BranchNode])

        node_list = []
        # key=lambda x: x[1] 是一个排序
        for moudule_name, _ in inspect.getmembers(node.op, inspect.ismodule):
            # print(moudule_name)
            for cls_name, cls in inspect.getmembers(sys.modules[f'node.op.{moudule_name}'], inspect.isclass):
                if cls_name != 'Node' and issubclass(cls, Node):
                    node_list.append(cls)
        NodeList.registerNode(node_list)

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
