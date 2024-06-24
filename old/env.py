import inspect
import os
import sys
from collections import defaultdict

from node.nlist import NodeList
from vg_node import Node


class Env:
    @staticmethod
    def registerNode():
        node_list = []

        # inspect只能查看Live Modules, 也就是必须是import过的
        # 如果想自动扫描路径下的所有node，自动注册，只用inspect是不行的
        sub_modules = []
        path_folder = os.path.dirname(__file__) + '/node/op'
        for module in os.listdir(path_folder):
            if not module.endswith('.py') or module == '__init__.py':
                continue
            __import__(f'node.op.{module[:-3]}')
            sub_modules.append(f'node.op.{module[:-3]}')

        for moudule_name in sub_modules:
            for cls_name, cls in inspect.getmembers(sys.modules[moudule_name], inspect.isclass):
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
